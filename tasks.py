import asyncio
import random


async def task_a(delay: float = 1.0, failure_rate: float = 0.1, **kwargs):
    """
    A sample async task that simulates work.

    Args:
        delay: Time to sleep in seconds
        failure_rate: Probability of task failure (0-1)
    """
    await asyncio.sleep(delay)
    if random.random() < failure_rate:
        raise Exception("Task A failed randomly")
    return {"message": "Task A completed successfully", "input_args": kwargs}


async def task_b(delay: float = 2.0, **kwargs):
    """
    A sample async task that always succeeds.

    Args:
        delay: Time to sleep in seconds
    """
    await asyncio.sleep(delay)
    return {"message": "Task B completed successfully", "input_args": kwargs}


async def task_c(delay: float = 1.5, raise_error: bool = False, **kwargs):
    """
    A sample async task that can be configured to fail.

    Args:
        delay: Time to sleep in seconds
        raise_error: If True, the task will fail
    """
    await asyncio.sleep(delay)
    if raise_error:
        raise Exception("Task C failed as requested")
    return {"message": "Task C completed successfully", "input_args": kwargs}
