"""
Data models for the Smart Meeting Assistant API

Defines the core data structures for meetings, transcripts, summaries,
action items, and decisions.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class ActionItem(BaseModel):
    """Represents an action item extracted from a meeting."""
    
    text: str = Field(..., description="The action item description")
    assignee: Optional[str] = Field(None, description="Person responsible for the action")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    deadline: Optional[datetime] = Field(None, description="Due date for the action")
    needs_clarification: bool = Field(False, description="Whether this item needs user clarification")


class Decision(BaseModel):
    """Represents a key decision made during a meeting."""
    
    decision: str = Field(..., description="The decision that was made")
    context: str = Field(..., description="Context around the decision")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    timestamp: Optional[str] = Field(None, description="When in the meeting this occurred")


class Summary(BaseModel):
    """Represents a meeting summary with extracted information."""
    
    meeting_id: str = Field(..., description="Unique identifier for the meeting")
    summary_text: str = Field(..., description="Overall summary of the meeting")
    key_points: List[str] = Field(default_factory=list, description="List of key discussion points")
    action_items: List[ActionItem] = Field(default_factory=list, description="Extracted action items")
    decisions: List[Decision] = Field(default_factory=list, description="Key decisions made")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="When summary was generated")


class Transcript(BaseModel):
    """Represents a meeting transcript."""
    
    meeting_id: str = Field(..., description="Unique identifier for the meeting")
    text: str = Field(..., description="Full transcript text")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall transcription confidence")
    language: str = Field(default="en", description="Language code")
    duration_seconds: Optional[int] = Field(None, description="Meeting duration in seconds")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When transcript was created")


class MeetingMetadata(BaseModel):
    """Metadata about a meeting."""
    
    meeting_id: str = Field(..., description="Unique identifier for the meeting")
    title: str = Field(..., description="Meeting title")
    participants: List[str] = Field(default_factory=list, description="List of participant names/emails")
    start_time: datetime = Field(..., description="When the meeting started")
    end_time: Optional[datetime] = Field(None, description="When the meeting ended")
    platform: str = Field(default="zoom", description="Meeting platform (zoom, gmeet, etc.)")


class ProcessMeetingRequest(BaseModel):
    """Request to process a meeting recording."""
    
    audio_file_path: str = Field(..., description="Path to the audio file")
    metadata: MeetingMetadata = Field(..., description="Meeting metadata")
    auto_summarize: bool = Field(default=True, description="Whether to automatically generate summary")


class ProcessMeetingResponse(BaseModel):
    """Response from processing a meeting."""
    
    meeting_id: str = Field(..., description="Unique identifier for the meeting")
    status: str = Field(..., description="Processing status (processing, completed, failed)")
    message: str = Field(..., description="Status message")
    transcript: Optional[Transcript] = Field(None, description="Transcript if available")
    summary: Optional[Summary] = Field(None, description="Summary if available")
