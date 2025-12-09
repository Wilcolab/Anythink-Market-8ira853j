"""Data models for meeting transcription and summarization."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ActionItem(BaseModel):
    """Represents an action item extracted from a meeting."""
    description: str = Field(..., description="The action item description")
    assignee: Optional[str] = Field(None, description="Person assigned to the action")
    confidence_score: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score for this extraction"
    )
    needs_clarification: bool = Field(
        False, description="Whether this item needs clarification"
    )


class MeetingSummary(BaseModel):
    """Represents a summary of a meeting."""
    key_points: List[str] = Field(
        default_factory=list, description="Key discussion points from the meeting"
    )
    decisions: List[str] = Field(
        default_factory=list, description="Decisions made during the meeting"
    )
    action_items: List[ActionItem] = Field(
        default_factory=list, description="Extracted action items"
    )


class MeetingTranscript(BaseModel):
    """Represents a full meeting transcript."""
    meeting_id: str = Field(..., description="Unique identifier for the meeting")
    transcript_text: str = Field(..., description="Full transcript of the meeting")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="When the transcript was created"
    )
    duration_minutes: Optional[int] = Field(
        None, description="Duration of the meeting in minutes"
    )
    participants: List[str] = Field(
        default_factory=list, description="List of meeting participants"
    )


class ProcessedMeeting(BaseModel):
    """Complete processed meeting data including transcript and summary."""
    meeting_id: str = Field(..., description="Unique identifier for the meeting")
    transcript: MeetingTranscript = Field(..., description="Meeting transcript")
    summary: MeetingSummary = Field(..., description="Meeting summary")
    processing_timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the meeting was processed"
    )
