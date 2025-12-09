"""Main processor for handling meeting end events and orchestrating transcription/summarization."""

import logging
from typing import Optional, Tuple
from datetime import datetime

from .models import Meeting, Transcription, Summary, MeetingStatus
from .transcription_service import TranscriptionService
from .summarization_service import SummarizationService

logger = logging.getLogger(__name__)


class MeetingProcessor:
    """
    Orchestrates the complete flow of processing a meeting after it ends.
    
    This includes:
    1. Transcribing the meeting audio
    2. Summarizing the transcription
    3. Extracting action items and decisions
    """
    
    def __init__(self):
        """Initialize the meeting processor with required services."""
        self.transcription_service = TranscriptionService()
        self.summarization_service = SummarizationService()
        
    def process_meeting_end(self, meeting: Meeting) -> Tuple[Optional[Transcription], Optional[Summary]]:
        """
        Process a meeting after it ends.
        
        This is the main entry point for automatic processing when a meeting ends.
        
        Args:
            meeting: Meeting object representing the ended meeting
            
        Returns:
            Tuple of (Transcription, Summary) if successful, (None, None) if failed
        """
        # Validate meeting object
        if not meeting:
            logger.error("Meeting object is None")
            return None, None
        
        if not hasattr(meeting, 'id') or not meeting.id:
            logger.error("Meeting object missing required field: id")
            return None, None
        
        if not hasattr(meeting, 'status'):
            logger.error(f"Meeting {meeting.id} missing status field")
            return None, None
        
        if meeting.status != MeetingStatus.ENDED:
            logger.warning(f"Cannot process meeting {meeting.id} - status is {meeting.status}, not ENDED")
            return None, None
        
        logger.info(f"Processing meeting {meeting.id} after call ended")
        
        # Step 1: Transcribe the meeting
        meeting.status = MeetingStatus.TRANSCRIBING
        transcription = self.transcription_service.transcribe_meeting(meeting)
        
        if not transcription:
            logger.error(f"Failed to transcribe meeting {meeting.id}")
            meeting.status = MeetingStatus.FAILED
            return None, None
        
        meeting.status = MeetingStatus.TRANSCRIBED
        logger.info(f"Meeting {meeting.id} transcribed successfully")
        
        # Step 2: Summarize the transcription
        summary = self.summarization_service.summarize_meeting(transcription)
        
        if not summary:
            logger.error(f"Failed to summarize meeting {meeting.id}")
            meeting.status = MeetingStatus.FAILED
            return transcription, None
        
        meeting.status = MeetingStatus.SUMMARIZED
        logger.info(f"Meeting {meeting.id} summarized successfully")
        
        # Log the results
        self._log_results(meeting, transcription, summary)
        
        return transcription, summary
    
    def _log_results(self, meeting: Meeting, transcription: Transcription, summary: Summary) -> None:
        """
        Log the processing results for debugging and monitoring.
        
        Args:
            meeting: Processed meeting
            transcription: Generated transcription
            summary: Generated summary
        """
        logger.info(f"""
        Meeting Processing Complete:
        - Meeting ID: {meeting.id}
        - Title: {meeting.title}
        - Transcription length: {len(transcription.text)} characters
        - Key points: {len(summary.key_points)}
        - Decisions: {len(summary.decisions)}
        - Action items: {len(summary.action_items)}
        - Processing completed at: {summary.timestamp}
        """)
        
        if summary.action_items:
            logger.info(f"Action items extracted:")
            for i, item in enumerate(summary.action_items, 1):
                logger.info(f"  {i}. {item.description} (Assignee: {item.assignee}, Confidence: {item.confidence_score:.2f})")
