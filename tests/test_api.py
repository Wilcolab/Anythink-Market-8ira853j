"""
Integration tests for the FastAPI application
"""

import pytest
import tempfile
import os
from datetime import datetime
from fastapi.testclient import TestClient
from sparkfleet_predictive_maintenance_api.main import app


class TestAPI:
    """Test cases for the REST API endpoints."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = TestClient(app)
    
    def test_root_endpoint(self):
        """Test the root endpoint returns API information."""
        response = self.client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "meeting-assistant"
    
    def test_process_meeting_success(self):
        """Test successful meeting processing."""
        # Create a temporary audio file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(b'test audio content')
            temp_file = f.name
        
        try:
            request_data = {
                "audio_file_path": temp_file,
                "metadata": {
                    "meeting_id": "api_test_001",
                    "title": "API Test Meeting",
                    "participants": ["Alice", "Bob"],
                    "start_time": datetime.utcnow().isoformat(),
                    "platform": "zoom"
                },
                "auto_summarize": True
            }
            
            response = self.client.post("/meetings/process", json=request_data)
            assert response.status_code == 200
            
            data = response.json()
            assert data["meeting_id"] == "api_test_001"
            assert data["status"] == "completed"
            assert "transcript" in data
            assert "summary" in data
            
            # Verify transcript structure
            transcript = data["transcript"]
            assert transcript["meeting_id"] == "api_test_001"
            assert "text" in transcript
            assert "confidence" in transcript
            
            # Verify summary structure
            summary = data["summary"]
            assert summary["meeting_id"] == "api_test_001"
            assert "summary_text" in summary
            assert "action_items" in summary
            assert "decisions" in summary
            
        finally:
            os.unlink(temp_file)
    
    def test_process_meeting_without_summary(self):
        """Test meeting processing without auto-summarization."""
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(b'audio')
            temp_file = f.name
        
        try:
            request_data = {
                "audio_file_path": temp_file,
                "metadata": {
                    "meeting_id": "no_summary_test",
                    "title": "Test Meeting",
                    "participants": ["Alice"],
                    "start_time": datetime.utcnow().isoformat(),
                    "platform": "gmeet"
                },
                "auto_summarize": False
            }
            
            response = self.client.post("/meetings/process", json=request_data)
            assert response.status_code == 200
            
            data = response.json()
            assert data["transcript"] is not None
            assert data["summary"] is None
            
        finally:
            os.unlink(temp_file)
    
    def test_process_meeting_invalid_file(self):
        """Test meeting processing with non-existent file."""
        request_data = {
            "audio_file_path": "/nonexistent/file.mp3",
            "metadata": {
                "meeting_id": "invalid_file_test",
                "title": "Test",
                "participants": [],
                "start_time": datetime.utcnow().isoformat()
            },
            "auto_summarize": True
        }
        
        response = self.client.post("/meetings/process", json=request_data)
        assert response.status_code == 400
    
    def test_get_transcript_success(self):
        """Test retrieving a transcript."""
        # First, process a meeting
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(b'audio')
            temp_file = f.name
        
        try:
            request_data = {
                "audio_file_path": temp_file,
                "metadata": {
                    "meeting_id": "transcript_test",
                    "title": "Test",
                    "participants": [],
                    "start_time": datetime.utcnow().isoformat()
                },
                "auto_summarize": True
            }
            
            self.client.post("/meetings/process", json=request_data)
            
            # Now retrieve the transcript
            response = self.client.get("/meetings/transcript_test/transcript")
            assert response.status_code == 200
            
            data = response.json()
            assert data["meeting_id"] == "transcript_test"
            assert "text" in data
            
        finally:
            os.unlink(temp_file)
    
    def test_get_transcript_not_found(self):
        """Test retrieving transcript for non-existent meeting."""
        response = self.client.get("/meetings/nonexistent/transcript")
        assert response.status_code == 404
    
    def test_get_summary_success(self):
        """Test retrieving a summary."""
        # First, process a meeting
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(b'audio')
            temp_file = f.name
        
        try:
            request_data = {
                "audio_file_path": temp_file,
                "metadata": {
                    "meeting_id": "summary_test",
                    "title": "Test",
                    "participants": [],
                    "start_time": datetime.utcnow().isoformat()
                },
                "auto_summarize": True
            }
            
            self.client.post("/meetings/process", json=request_data)
            
            # Now retrieve the summary
            response = self.client.get("/meetings/summary_test/summary")
            assert response.status_code == 200
            
            data = response.json()
            assert data["meeting_id"] == "summary_test"
            assert "summary_text" in data
            assert "action_items" in data
            assert "decisions" in data
            
        finally:
            os.unlink(temp_file)
    
    def test_get_summary_not_found(self):
        """Test retrieving summary for non-existent meeting."""
        response = self.client.get("/meetings/nonexistent/summary")
        assert response.status_code == 404
    
    def test_get_summary_without_auto_summarize(self):
        """Test retrieving summary when not generated."""
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(b'audio')
            temp_file = f.name
        
        try:
            request_data = {
                "audio_file_path": temp_file,
                "metadata": {
                    "meeting_id": "no_auto_summary",
                    "title": "Test",
                    "participants": [],
                    "start_time": datetime.utcnow().isoformat()
                },
                "auto_summarize": False
            }
            
            self.client.post("/meetings/process", json=request_data)
            
            # Try to retrieve summary (should fail)
            response = self.client.get("/meetings/no_auto_summary/summary")
            assert response.status_code == 404
            
        finally:
            os.unlink(temp_file)
    
    def test_list_meetings(self):
        """Test listing all processed meetings."""
        # Process a meeting first
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(b'audio')
            temp_file = f.name
        
        try:
            request_data = {
                "audio_file_path": temp_file,
                "metadata": {
                    "meeting_id": "list_test",
                    "title": "Test",
                    "participants": [],
                    "start_time": datetime.utcnow().isoformat()
                },
                "auto_summarize": True
            }
            
            self.client.post("/meetings/process", json=request_data)
            
            # List meetings
            response = self.client.get("/meetings")
            assert response.status_code == 200
            
            data = response.json()
            assert isinstance(data, dict)
            assert "list_test" in data
            
        finally:
            os.unlink(temp_file)
