"""Main meeting processor that coordinates transcription and summarization."""
from datetime import datetime
from typing import Optional, List
import logging
from .models import MeetingTranscript, ProcessedMeeting
from .transcription_service import TranscriptionService
from .summarization_service import SummarizationService

logger = logging.getLogger(__name__)


class MeetingProcessor:
    """
    Coordinates the processing of meetings after they end.
    
    This includes transcription, summarization, and action item extraction.
    """

    def __init__(
        self,
        transcription_service: Optional[TranscriptionService] = None,
        summarization_service: Optional[SummarizationService] = None
    ):
        """
        Initialize the meeting processor.

        Args:
            transcription_service: Service for transcribing audio
            summarization_service: Service for summarizing transcripts
        """
        self.transcription_service = transcription_service or TranscriptionService()
        self.summarization_service = summarization_service or SummarizationService()
        logger.info("Initialized MeetingProcessor")

    def process_meeting(
        self,
        meeting_id: str,
        audio_file_path: str,
        participants: Optional[List[str]] = None,
        duration_minutes: Optional[int] = None
    ) -> ProcessedMeeting:
        """
        Process a meeting after it ends.

        This is the main entry point that:
        1. Transcribes the meeting audio
        2. Generates a summary with key points and decisions
        3. Extracts action items

        Args:
            meeting_id: Unique identifier for the meeting
            audio_file_path: Path to the meeting audio file
            participants: List of meeting participants
            duration_minutes: Duration of the meeting in minutes

        Returns:
            ProcessedMeeting object containing transcript and summary

        Raises:
            ValueError: If the audio file is invalid
        """
        logger.info(f"Processing meeting {meeting_id}")
        
        # Validate audio file
        if not self.transcription_service.validate_audio_file(audio_file_path):
            raise ValueError(f"Invalid audio file: {audio_file_path}")
        
        # Step 1: Transcribe the audio
        logger.info(f"Step 1: Transcribing audio for meeting {meeting_id}")
        transcript_text = self.transcription_service.transcribe_audio(
            audio_file_path, meeting_id
        )
        
        # Create transcript object
        transcript = MeetingTranscript(
            meeting_id=meeting_id,
            transcript_text=transcript_text,
            timestamp=datetime.utcnow(),
            duration_minutes=duration_minutes,
            participants=participants or []
        )
        
        # Step 2: Summarize the transcript
        logger.info(f"Step 2: Summarizing transcript for meeting {meeting_id}")
        summary = self.summarization_service.summarize_transcript(transcript_text)
        
        # Create processed meeting object
        processed_meeting = ProcessedMeeting(
            meeting_id=meeting_id,
            transcript=transcript,
            summary=summary,
            processing_timestamp=datetime.utcnow()
        )
        
        logger.info(
            f"Successfully processed meeting {meeting_id}. "
            f"Extracted {len(summary.key_points)} key points, "
            f"{len(summary.decisions)} decisions, and "
            f"{len(summary.action_items)} action items."
        )
        
        return processed_meeting

    def process_meeting_on_call_end(
        self,
        meeting_id: str,
        audio_file_path: str,
        participants: Optional[List[str]] = None,
        duration_minutes: Optional[int] = None
    ) -> ProcessedMeeting:
        """
        Event handler that triggers when a call ends.

        This is typically called by Zoom/GMeet integration when a meeting ends.

        Args:
            meeting_id: Unique identifier for the meeting
            audio_file_path: Path to the meeting audio file
            participants: List of meeting participants
            duration_minutes: Duration of the meeting in minutes

        Returns:
            ProcessedMeeting object containing transcript and summary
        """
        logger.info(f"Meeting {meeting_id} ended. Starting automatic processing...")
        return self.process_meeting(
            meeting_id=meeting_id,
            audio_file_path=audio_file_path,
            participants=participants,
            duration_minutes=duration_minutes
        )
