from enum import Enum
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator


class TaskStatus(str, Enum):
    """Status of a task in the workflow"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ExecutionMode(str, Enum):
    """Mode of execution for steps in a workflow"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"


class Task(BaseModel):
    """
    Represents a single task in the workflow

    Attributes:
        name: Unique identifier/name for the task
        task_id: Function identifier that maps to an actual task implementation
        parameters: Optional parameters to pass to the task
        status: Current status of the task
        depends_on: Optional list of task names that must complete before this task
    """
    name: str = Field(..., min_length=1,
                      description="Unique name for the task")
    task_id: str = Field(..., min_length=1,
                         description="Function identifier for the task")
    parameters: Optional[Dict] = Field(
        default=None, description="Optional parameters for the task")
    status: TaskStatus = Field(
        default=TaskStatus.PENDING, description="Current status of the task")
    depends_on: Optional[List[str]] = Field(
        default=None, description="Tasks that must complete before this one")

    @field_validator("task_id")
    @classmethod
    def validate_task_id(cls, v):
        """Ensure task_id refers to a valid task function"""
        valid_tasks = ["task_a", "task_b",
                       "task_c"]  # This should be dynamic in production
        if v not in valid_tasks:
            raise ValueError(f"task_id must be one of: {valid_tasks}")
        return v


class Step(BaseModel):
    """
    Represents a group of tasks or nested steps that can be executed together

    Attributes:
        name: Name of the step
        execution_mode: Whether tasks/steps should run sequentially or in parallel
        tasks: List of tasks in this step
        steps: List of nested steps
        condition: Optional condition for executing this step
    """
    name: str = Field(..., min_length=1, description="Name of the step")
    execution_mode: ExecutionMode = Field(
        default=ExecutionMode.SEQUENTIAL,
        description="Whether tasks run sequentially or in parallel"
    )
    tasks: Optional[List[Task]] = Field(
        default=None, description="Tasks in this step")
    steps: Optional[List["Step"]] = Field(
        default=None, description="Nested steps")
    condition: Optional[str] = Field(
        default=None,
        description="Optional condition for step execution"
    )

    @field_validator("steps")
    @classmethod
    def validate_steps(cls, v, values):
        """Ensure either tasks or steps are defined, but not both empty"""
        data = values.data
        tasks = data.get("tasks")
        if (not tasks and not v) or (tasks and v):
            raise ValueError(
                "Either tasks or steps must be defined, but not both")
        return v


class Workflow(BaseModel):
    """
    Root workflow definition that contains all steps and metadata

    Attributes:
        name: Name of the workflow
        description: Optional description of what the workflow does
        version: Version number of the workflow
        steps: List of steps in the workflow
    """
    name: str = Field(..., min_length=1, description="Name of the workflow")
    description: Optional[str] = Field(
        default=None, description="Description of the workflow")
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$",
                         description="Semantic version number")
    steps: List[Step] = Field(..., min_length=1,
                              description="Steps in the workflow")


# Update forward references for nested models
Step.model_rebuild()
