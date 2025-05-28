"""Redis service for workflow persistence."""
from typing import Dict, Optional
import json
from redis import Redis, ConnectionError
from pydantic import BaseModel


class RedisService:
    """Service for interacting with Redis."""

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """Initialize Redis connection."""
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)
        self._test_connection()

    def _test_connection(self):
        """Test Redis connection."""
        try:
            self.redis.ping()
        except ConnectionError as e:
            raise ConnectionError("Failed to connect to Redis") from e

    def _get_run_key(self, run_id: str) -> str:
        """Get Redis key for a workflow run."""
        return f"workflow:run:{run_id}"

    def _get_task_key(self, run_id: str, task_name: str) -> str:
        """Get Redis key for a task within a workflow run."""
        return f"workflow:run:{run_id}:task:{task_name}"

    def store_workflow_status(self, run_id: str, status: Dict) -> None:
        """Store workflow run status in Redis."""
        key = self._get_run_key(run_id)
        self.redis.hmset(key, {
            "status": status["status"],
            "data": json.dumps(status.get("data", {}))
        })
        # Set expiry to 24 hours to prevent Redis from filling up
        self.redis.expire(key, 86400)

    def get_workflow_status(self, run_id: str) -> Optional[Dict]:
        """Get workflow run status from Redis."""
        key = self._get_run_key(run_id)
        data = self.redis.hgetall(key)
        if not data:
            return None

        return {
            "status": data["status"],
            "data": json.loads(data["data"])
        }

    def store_task_result(self, run_id: str, task_name: str, result: Dict) -> None:
        """Store task execution result in Redis."""
        key = self._get_task_key(run_id, task_name)
        self.redis.hmset(key, {
            "status": result["status"],
            "result": json.dumps(result.get("result", {})),
            "error": result.get("error", "")
        })
        self.redis.expire(key, 86400)  # 24 hour expiry

    def get_task_result(self, run_id: str, task_name: str) -> Optional[Dict]:
        """Get task execution result from Redis."""
        key = self._get_task_key(run_id, task_name)
        data = self.redis.hgetall(key)
        if not data:
            return None

        return {
            "status": data["status"],
            "result": json.loads(data["result"]),
            "error": data.get("error", "")
        }
