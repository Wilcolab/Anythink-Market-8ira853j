from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from workflow.schema import Workflow
from workflow.engine import WorkflowEngine
from workflow.redis_service import RedisService
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
try:
    redis_service = RedisService()
    workflow_engine = WorkflowEngine(redis_service)
except Exception as e:
    logger.error(f"Failed to initialize services: {e}")
    raise


@app.get("/")
def root():
    return JSONResponse({
        "status": "success",
        "message": "Welcome to the Workflow Engine API!",
    })


@app.post("/workflow")
async def trigger_workflow(workflow: Workflow):
    """
    Trigger a new workflow execution.
    Returns a run ID for tracking the workflow status.
    """
    try:
        run_id = await workflow_engine.execute_workflow(workflow)
        return JSONResponse({
            "status": "success",
            "run_id": run_id,
            "message": "Workflow execution started"
        })
    except Exception as e:
        logger.exception("Failed to start workflow")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflow/{run_id}")
def get_workflow_status(run_id: str):
    """Get the status of a workflow execution."""
    try:
        status = redis_service.get_workflow_status(run_id)
        if not status:
            raise HTTPException(
                status_code=404, detail="Workflow run not found")

        # Get all task results for this workflow
        tasks = {}
        workflow_data = status["data"]
        for task_key in redis_service.redis.scan_iter(f"workflow:run:{run_id}:task:*"):
            task_name = task_key.split(":")[-1]
            task_result = redis_service.get_task_result(run_id, task_name)
            if task_result:
                tasks[task_name] = task_result

        return JSONResponse({
            "status": "success",
            "data": {
                "workflow_status": status["status"],
                "workflow_data": workflow_data,
                "tasks": tasks
            }
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to get workflow status")
        raise HTTPException(status_code=500, detail=str(e))
