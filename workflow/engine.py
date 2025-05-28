"""Async workflow execution engine."""
import asyncio
import uuid
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime
from .schema import Workflow, Step, Task, TaskStatus, ExecutionMode
from .redis_service import RedisService
from .resilience import CircuitBreaker, with_retry
import tasks

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """Async workflow execution engine."""

    def __init__(self, redis_service: RedisService):
        """Initialize workflow engine."""
        self.redis = redis_service
        self._task_registry = {
            "task_a": tasks.task_a,
            "task_b": tasks.task_b,
            "task_c": tasks.task_c
        }
        self._running_tasks: Dict[str, Dict[str, asyncio.Task]] = {}
        # Initialize circuit breakers for each task
        self._circuit_breakers: Dict[str, CircuitBreaker] = {
            task_id: CircuitBreaker(failure_threshold=5, reset_timeout=60)
            for task_id in self._task_registry.keys()
        }

    async def execute_workflow(self, workflow: Workflow) -> str:
        """
        Execute a workflow asynchronously.

        Returns:
            str: The run ID for tracking the workflow execution
        """
        run_id = str(uuid.uuid4())
        self._running_tasks[run_id] = {}

        # Initialize workflow status in Redis
        self.redis.store_workflow_status(run_id, {
            "status": "running",
            "data": {
                "name": workflow.name,
                "version": workflow.version,
                "start_time": datetime.utcnow().isoformat(),
                "step_count": len(workflow.steps)
            }
        })

        # Start workflow execution in background
        asyncio.create_task(self._execute_workflow(workflow, run_id))
        return run_id

    async def _execute_workflow(self, workflow: Workflow, run_id: str) -> None:
        """Execute workflow steps and handle failures."""
        try:
            for step in workflow.steps:
                success = await self._execute_step(step, run_id)
                if not success:
                    await self._mark_workflow_failed(run_id)
                    return

            await self._mark_workflow_completed(run_id)
        except Exception as e:
            logger.exception("Workflow execution failed")
            await self._mark_workflow_failed(run_id, str(e))

    async def _execute_step(self, step: Step, run_id: str) -> bool:
        """
        Execute a workflow step.

        Returns:
            bool: True if step executed successfully, False otherwise
        """
        if step.steps:  # Handle nested steps
            if step.execution_mode == ExecutionMode.PARALLEL:
                return await self._execute_parallel_steps(step.steps, run_id)
            return await self._execute_sequential_steps(step.steps, run_id)

        if step.tasks:  # Handle tasks
            if step.execution_mode == ExecutionMode.PARALLEL:
                return await self._execute_parallel_tasks(step.tasks, run_id)
            return await self._execute_sequential_tasks(step.tasks, run_id)

        return True

    async def _execute_sequential_steps(self, steps: List[Step], run_id: str) -> bool:
        """Execute steps sequentially."""
        for step in steps:
            success = await self._execute_step(step, run_id)
            if not success:
                return False
        return True

    async def _execute_parallel_steps(self, steps: List[Step], run_id: str) -> bool:
        """Execute steps in parallel."""
        tasks = [self._execute_step(step, run_id) for step in steps]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return all(isinstance(r, bool) and r for r in results)

    async def _execute_sequential_tasks(self, tasks: List[Task], run_id: str) -> bool:
        """Execute tasks sequentially."""
        for task in tasks:
            success = await self._execute_task(task, run_id)
            if not success:
                return False
        return True

    async def _execute_parallel_tasks(self, tasks: List[Task], run_id: str) -> bool:
        """Execute tasks in parallel."""
        async_tasks = [self._execute_task(task, run_id) for task in tasks]
        results = await asyncio.gather(*async_tasks, return_exceptions=True)
        return all(isinstance(r, bool) and r for r in results)

    async def _execute_task(self, task: Task, run_id: str) -> bool:
        """Execute a single task."""
        try:
            # Check dependencies
            if task.depends_on:
                for dep in task.depends_on:
                    dep_result = self.redis.get_task_result(run_id, dep)
                    if not dep_result or dep_result["status"] != "completed":
                        await self._store_task_status(run_id, task, "skipped",
                                                    error="Dependencies not met")
                        return False

            await self._store_task_status(run_id, task, "running")

            # Get task function
            task_func = self._task_registry.get(task.task_id)
            if not task_func:
                raise ValueError(f"Task {task.task_id} not found in registry")

            # Execute task with retry and circuit breaker
            result = await with_retry(
                task_func,
                max_retries=3,  # Configurable
                initial_delay=1.0,  # Start with 1 second delay
                max_delay=30.0,  # Cap at 30 seconds
                exponential_base=2.0,  # Double the delay each time
                circuit_breaker=self._circuit_breakers[task.task_id],
                **(task.parameters or {})
            )

            await self._store_task_status(run_id, task, "completed", result=result)
            return True

        except Exception as e:
            logger.exception(f"Task {task.name} failed")
            await self._store_task_status(run_id, task, "failed", error=str(e))
            return False

    async def _store_task_status(self, run_id: str, task: Task,
                                 status: str, result: Any = None,
                                 error: Optional[str] = None) -> None:
        """Store task status in Redis."""
        self.redis.store_task_result(run_id, task.name, {
            "status": status,
            "result": result or {},
            "error": error or ""
        })

    async def _mark_workflow_completed(self, run_id: str) -> None:
        """Mark workflow as completed."""
        self.redis.store_workflow_status(run_id, {
            "status": "completed",
            "data": {
                "end_time": datetime.utcnow().isoformat()
            }
        })

    async def _mark_workflow_failed(self, run_id: str, error: str = "") -> None:
        """Mark workflow as failed."""
        self.redis.store_workflow_status(run_id, {
            "status": "failed",
            "data": {
                "end_time": datetime.utcnow().isoformat(),
                "error": error
            }
        })
