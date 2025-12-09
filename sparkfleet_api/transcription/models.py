"""Data models for meeting transcription and summarization."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class MeetingPlatform(Enum):
    """Supported meeting platforms."""
    ZOOM = "zoom"
    GMEET = "gmeet"


class MeetingStatus(Enum):
    """Meeting processing status."""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    ENDED = "ended"
    TRANSCRIBING = "transcribing"
    TRANSCRIBED = "transcribed"
    SUMMARIZED = "summarized"
    FAILED = "failed"


@dataclass
class Meeting:
    """Represents a meeting session."""
    id: str
    title: str
    platform: MeetingPlatform
    start_time: datetime
    end_time: Optional[datetime] = None
    status: MeetingStatus = MeetingStatus.SCHEDULED
    participants: List[str] = field(default_factory=list)
    audio_url: Optional[str] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class Transcription:
    """Represents the transcription of a meeting."""
    meeting_id: str
    text: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    language: str = "en"
    confidence_score: float = 0.0
    segments: List[dict] = field(default_factory=list)


@dataclass
class ActionItem:
    """Represents an action item extracted from meeting."""
    description: str
    assignee: Optional[str] = None
    confidence_score: float = 0.0
    deadline: Optional[datetime] = None
    source_segment: Optional[str] = None


@dataclass
class Summary:
    """Represents the summary of a meeting."""
    meeting_id: str
    key_points: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    action_items: List[ActionItem] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    summary_text: Optional[str] = None
