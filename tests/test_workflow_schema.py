import pytest
from pydantic import ValidationError
from workflow.schema import Workflow, Step, Task, ExecutionMode, TaskStatus


def test_valid_simple_workflow():
    """Test a simple sequential workflow"""
    workflow_data = {
        "name": "Simple Workflow",
        "version": "1.0.0",
        "steps": [{
            "name": "Single Step",
            "tasks": [{
                "name": "Task A",
                "task_id": "task_a"
            }]
        }]
    }
    workflow = Workflow(**workflow_data)
    assert workflow.name == "Simple Workflow"
    assert workflow.version == "1.0.0"
    assert len(workflow.steps) == 1
    assert workflow.steps[0].tasks[0].status == TaskStatus.PENDING


def test_valid_complex_workflow():
    """Test a complex workflow with nested steps and parallel execution"""
    workflow_data = {
        "name": "Complex Workflow",
        "description": "A complex workflow with nested steps",
        "version": "1.0.0",
        "steps": [{
            "name": "Parallel Steps",
            "execution_mode": "parallel",
            "steps": [{
                "name": "Branch 1",
                "tasks": [{
                    "name": "Task A",
                    "task_id": "task_a",
                    "parameters": {"param1": "value1"}
                }]
            }, {
                "name": "Branch 2",
                "tasks": [{
                    "name": "Task B",
                    "task_id": "task_b",
                    "depends_on": ["Task A"]
                }]
            }]
        }]
    }
    workflow = Workflow(**workflow_data)
    assert workflow.steps[0].execution_mode == ExecutionMode.PARALLEL
    assert len(workflow.steps[0].steps) == 2


def test_invalid_task_id():
    """Test that invalid task_id raises ValidationError"""
    with pytest.raises(ValidationError) as exc_info:
        Task(name="Invalid Task", task_id="nonexistent_task")
    assert "task_id must be one of" in str(exc_info.value)


def test_invalid_step_definition():
    """Test that a step with both tasks and steps raises ValidationError"""
    with pytest.raises(ValidationError) as exc_info:
        Step(
            name="Invalid Step",
            tasks=[Task(name="Task A", task_id="task_a")],
            steps=[Step(name="Sub Step", tasks=[
                        Task(name="Task B", task_id="task_b")])]
        )
    assert "Either tasks or steps must be defined" in str(exc_info.value)


def test_invalid_version_format():
    """Test that invalid version format raises ValidationError"""
    with pytest.raises(ValidationError) as exc_info:
        Workflow(
            name="Invalid Version",
            version="1.0",
            steps=[Step(name="Step", tasks=[
                        Task(name="Task", task_id="task_a")])]
        )
    assert "pattern" in str(exc_info.value)


def test_empty_workflow():
    """Test that workflow with no steps raises ValidationError"""
    with pytest.raises(ValidationError) as exc_info:
        Workflow(name="Empty Workflow", version="1.0.0", steps=[])
    assert "List should have at least 1 item" in str(exc_info.value)
