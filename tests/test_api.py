"""Tests for the FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from sparkfleet_api.main import app

client = TestClient(app)


class TestMeetingAPI:
    """Tests for the meeting API endpoints."""

    def test_root_endpoint(self):
        """Test the root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "features" in data

    def test_health_endpoint(self):
        """Test the health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_meetings_health_endpoint(self):
        """Test the meetings health endpoint."""
        response = client.get("/api/meetings/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "features" in data

    def test_process_meeting_endpoint(self):
        """Test the process meeting endpoint."""
        payload = {
            "meeting_id": "test-meeting-123",
            "audio_file_path": "/fake/path/test.mp3",
            "participants": ["Alice", "Bob"],
            "duration_minutes": 30
        }
        
        response = client.post("/api/meetings/process", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["meeting_id"] == "test-meeting-123"
        assert "transcript" in data
        assert "summary" in data
        assert "key_points" in data["summary"]
        assert "decisions" in data["summary"]
        assert "action_items" in data["summary"]

    def test_call_ended_webhook_endpoint(self):
        """Test the call ended webhook endpoint."""
        payload = {
            "meeting_id": "webhook-meeting-456",
            "audio_file_path": "/fake/path/webhook.mp3",
            "participants": ["User1", "User2"],
            "duration_minutes": 45
        }
        
        response = client.post("/api/meetings/webhook/call-ended", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["meeting_id"] == "webhook-meeting-456"
        assert "transcript" in data
        assert "summary" in data

    def test_process_meeting_without_optional_fields(self):
        """Test processing a meeting without optional fields."""
        payload = {
            "meeting_id": "minimal-meeting",
            "audio_file_path": "/fake/path/minimal.mp3"
        }
        
        response = client.post("/api/meetings/process", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["meeting_id"] == "minimal-meeting"

    def test_process_meeting_missing_required_fields(self):
        """Test that missing required fields returns 422."""
        payload = {
            "meeting_id": "incomplete-meeting"
            # Missing audio_file_path
        }
        
        response = client.post("/api/meetings/process", json=payload)
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
