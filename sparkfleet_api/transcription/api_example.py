"""
Example API endpoints for meeting transcription and summarization.

This demonstrates how to integrate the transcription system with a web framework.
In production, this would be integrated into a FastAPI or Flask application.
"""

import logging
from datetime import datetime
from typing import Dict, Any

from .webhook_handler import WebhookHandler
from .meeting_processor import MeetingProcessor
from .models import Meeting, MeetingPlatform, MeetingStatus

logger = logging.getLogger(__name__)


class TranscriptionAPI:
    """API interface for transcription and summarization functionality."""
    
    def __init__(self):
        """Initialize the API with required handlers."""
        self.webhook_handler = WebhookHandler()
        self.processor = MeetingProcessor()
    
    def webhook_meeting_ended(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        POST /api/webhooks/meeting-ended
        
        Webhook endpoint that receives notifications when meetings end.
        
        Args:
            payload: Webhook data from meeting platform
            
        Returns:
            Response with processing status
        """
        logger.info("Received meeting ended webhook")
        return self.webhook_handler.handle_meeting_ended(payload)
    
    def process_meeting_manually(self, meeting_id: str, audio_url: str) -> Dict[str, Any]:
        """
        POST /api/meetings/{meeting_id}/process
        
        Manually trigger processing for a meeting.
        
        Args:
            meeting_id: ID of the meeting to process
            audio_url: URL to the meeting audio recording
            
        Returns:
            Response with processing status
        """
        logger.info(f"Manual processing triggered for meeting {meeting_id}")
        
        # Create a meeting object
        meeting = Meeting(
            id=meeting_id,
            title="Manual Processing",
            platform=MeetingPlatform.ZOOM,
            start_time=datetime.utcnow(),
            status=MeetingStatus.ENDED,
            audio_url=audio_url
        )
        
        # Process the meeting
        transcription, summary = self.processor.process_meeting_end(meeting)
        
        if not transcription or not summary:
            return {
                "status": "error",
                "message": "Failed to process meeting"
            }
        
        return {
            "status": "success",
            "meeting_id": meeting_id,
            "transcription": {
                "text": transcription.text,
                "confidence": transcription.confidence_score
            },
            "summary": {
                "key_points": summary.key_points,
                "decisions": summary.decisions,
                "action_items": [
                    {
                        "description": item.description,
                        "assignee": item.assignee,
                        "confidence": item.confidence_score
                    }
                    for item in summary.action_items
                ],
                "full_summary": summary.summary_text
            }
        }


# Example usage demonstration
def example_usage():
    """Demonstrate how to use the API."""
    api = TranscriptionAPI()
    
    # Example 1: Webhook from Zoom when meeting ends
    zoom_webhook = {
        "platform": "zoom",
        "meeting_id": "123456789",
        "topic": "Q4 Planning Meeting",
        "start_time": "2024-01-15T10:00:00",
        "participants": ["alice@company.com", "bob@company.com"],
        "recording_url": "https://zoom.us/rec/play/abc123"
    }
    
    result = api.webhook_meeting_ended(zoom_webhook)
    print("Webhook processing result:", result)
    
    # Example 2: Manual processing
    result = api.process_meeting_manually(
        meeting_id="987654321",
        audio_url="https://storage.example.com/meeting-audio.mp3"
    )
    print("Manual processing result:", result)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    example_usage()
