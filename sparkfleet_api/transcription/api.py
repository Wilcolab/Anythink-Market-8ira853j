"""FastAPI endpoints for meeting transcription and summarization."""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
import logging
from .meeting_processor import MeetingProcessor
from .models import ProcessedMeeting

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/meetings", tags=["meetings"])

# Initialize the meeting processor
meeting_processor = MeetingProcessor()


class MeetingEndEvent(BaseModel):
    """Event data when a meeting ends."""
    meeting_id: str = Field(..., description="Unique identifier for the meeting")
    audio_file_path: str = Field(..., description="Path to the meeting audio file")
    participants: Optional[List[str]] = Field(
        None, description="List of meeting participants"
    )
    duration_minutes: Optional[int] = Field(
        None, description="Duration of the meeting in minutes"
    )


@router.post(
    "/process",
    response_model=ProcessedMeeting,
    status_code=status.HTTP_200_OK,
    summary="Process a meeting after it ends",
    description="Transcribe and summarize a meeting, extracting key points, decisions, and action items."
)
async def process_meeting(event: MeetingEndEvent) -> ProcessedMeeting:
    """
    Process a meeting after it ends.

    This endpoint:
    1. Transcribes the meeting audio
    2. Generates a summary with key points and decisions
    3. Extracts action items with confidence scores

    Args:
        event: Meeting end event data

    Returns:
        ProcessedMeeting containing transcript and summary

    Raises:
        HTTPException: If processing fails
    """
    try:
        logger.info(f"Received request to process meeting {event.meeting_id}")
        
        processed_meeting = meeting_processor.process_meeting(
            meeting_id=event.meeting_id,
            audio_file_path=event.audio_file_path,
            participants=event.participants,
            duration_minutes=event.duration_minutes
        )
        
        return processed_meeting
    
    except ValueError as e:
        logger.error(f"Validation error processing meeting {event.meeting_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error processing meeting {event.meeting_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process meeting: {str(e)}"
        )


@router.post(
    "/webhook/call-ended",
    response_model=ProcessedMeeting,
    status_code=status.HTTP_200_OK,
    summary="Webhook for call end events",
    description="Automatically process a meeting when a Zoom/GMeet call ends."
)
async def handle_call_ended_webhook(event: MeetingEndEvent) -> ProcessedMeeting:
    """
    Webhook endpoint that Zoom/GMeet integrations call when a meeting ends.

    This triggers automatic transcription and summarization.

    Args:
        event: Meeting end event data

    Returns:
        ProcessedMeeting containing transcript and summary

    Raises:
        HTTPException: If processing fails
    """
    try:
        logger.info(f"Call ended webhook received for meeting {event.meeting_id}")
        
        processed_meeting = meeting_processor.process_meeting_on_call_end(
            meeting_id=event.meeting_id,
            audio_file_path=event.audio_file_path,
            participants=event.participants,
            duration_minutes=event.duration_minutes
        )
        
        return processed_meeting
    
    except ValueError as e:
        logger.error(f"Validation error in webhook for meeting {event.meeting_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in webhook for meeting {event.meeting_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process meeting: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint"
)
async def health_check():
    """Check if the transcription service is operational."""
    return {
        "status": "healthy",
        "service": "meeting-transcription",
        "features": [
            "transcription",
            "summarization",
            "action_item_extraction"
        ]
    }
