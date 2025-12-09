"""Webhook handler for meeting platform events (Zoom/GMeet)."""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .models import Meeting, MeetingPlatform, MeetingStatus
from .meeting_processor import MeetingProcessor

logger = logging.getLogger(__name__)


class WebhookHandler:
    """
    Handles webhook events from meeting platforms (Zoom, GMeet).
    
    This receives notifications when meetings end and triggers
    automatic transcription and summarization.
    """
    
    def __init__(self):
        """Initialize the webhook handler."""
        self.processor = MeetingProcessor()
        
    def handle_meeting_ended(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a meeting ended webhook event.
        
        Args:
            webhook_data: Webhook payload from meeting platform
            
        Returns:
            Response dictionary with processing status
        """
        try:
            # Parse the webhook data into a Meeting object
            meeting = self._parse_webhook_data(webhook_data)
            
            if not meeting:
                return {
                    "status": "error",
                    "message": "Failed to parse webhook data"
                }
            
            logger.info(f"Received meeting ended event for meeting {meeting.id}")
            
            # Mark meeting as ended
            meeting.status = MeetingStatus.ENDED
            meeting.end_time = datetime.utcnow()
            
            # Process the meeting (transcribe and summarize)
            transcription, summary = self.processor.process_meeting_end(meeting)
            
            if not transcription or not summary:
                return {
                    "status": "error",
                    "message": "Failed to process meeting",
                    "meeting_id": meeting.id
                }
            
            return {
                "status": "success",
                "message": "Meeting processed successfully",
                "meeting_id": meeting.id,
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
                    ]
                }
            }
            
        except Exception as e:
            logger.error(f"Error handling meeting ended webhook: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _parse_webhook_data(self, webhook_data: Dict[str, Any]) -> Optional[Meeting]:
        """
        Parse webhook payload into a Meeting object.
        
        Args:
            webhook_data: Raw webhook data from platform
            
        Returns:
            Meeting object or None if parsing fails
        """
        try:
            # Handle different webhook formats from different platforms
            platform_str = webhook_data.get("platform", "zoom").lower()
            
            if platform_str == "zoom":
                platform = MeetingPlatform.ZOOM
            elif platform_str in ["gmeet", "google-meet"]:
                platform = MeetingPlatform.GMEET
            else:
                logger.warning(f"Unknown platform: {platform_str}, defaulting to ZOOM")
                platform = MeetingPlatform.ZOOM
            
            # Parse start_time safely
            start_time_str = webhook_data.get("start_time")
            if start_time_str:
                try:
                    start_time = datetime.fromisoformat(start_time_str)
                except (ValueError, TypeError):
                    logger.warning(f"Invalid start_time format: {start_time_str}, using current time")
                    start_time = datetime.utcnow()
            else:
                start_time = datetime.utcnow()
            
            meeting = Meeting(
                id=webhook_data.get("meeting_id", ""),
                title=webhook_data.get("topic", webhook_data.get("title", "Untitled Meeting")),
                platform=platform,
                start_time=start_time,
                participants=webhook_data.get("participants", []),
                audio_url=webhook_data.get("recording_url", webhook_data.get("audio_url")),
                metadata=webhook_data.get("metadata", {})
            )
            
            return meeting
            
        except Exception as e:
            logger.error(f"Error parsing webhook data: {str(e)}")
            return None
