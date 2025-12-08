"""
Meeting processing orchestration

Coordinates the transcription and summarization workflow for meetings.
"""

import logging
from datetime import datetime
from typing import Optional
from ..models import (
    Transcript, 
    Summary, 
    ActionItem, 
    Decision,
    MeetingMetadata
)
from .transcriber import Transcriber
from .summarizer import Summarizer

logger = logging.getLogger(__name__)


class MeetingProcessor:
    """
    Orchestrates the full meeting processing pipeline.
    
    Coordinates:
    1. Audio transcription
    2. Content summarization
    3. Action item extraction
    4. Decision extraction
    
    Designed to meet the 5-minute processing target from spec.md.
    """
    
    def __init__(self, transcriber: Optional[Transcriber] = None, 
                 summarizer: Optional[Summarizer] = None):
        """
        Initialize the meeting processor.
        
        Args:
            transcriber: Optional Transcriber instance (creates default if None)
            summarizer: Optional Summarizer instance (creates default if None)
        """
        self.transcriber = transcriber or Transcriber()
        self.summarizer = summarizer or Summarizer()
        logger.info("MeetingProcessor initialized")
    
    def process_meeting(
        self, 
        audio_file_path: str,
        metadata: MeetingMetadata,
        auto_summarize: bool = True
    ) -> tuple[Transcript, Optional[Summary]]:
        """
        Process a meeting recording end-to-end.
        
        This is the main entry point for automated meeting processing
        after a call ends, addressing the acceptance criterion:
        "Meetings can be transcribed and summarized automatically after call ends."
        
        Args:
            audio_file_path: Path to the audio recording file
            metadata: Meeting metadata (title, participants, etc.)
            auto_summarize: Whether to automatically generate summary (default: True)
            
        Returns:
            Tuple of (Transcript, Summary) - Summary may be None if auto_summarize=False
            
        Raises:
            Exception: If transcription or summarization fails
        """
        logger.info(f"Processing meeting {metadata.meeting_id}: {metadata.title}")
        start_time = datetime.utcnow()
        
        try:
            # Step 1: Transcribe audio
            logger.info(f"Step 1/2: Transcribing audio file: {audio_file_path}")
            transcription_result = self.transcriber.transcribe_audio(
                audio_file_path, 
                metadata.meeting_id
            )
            
            # Create transcript object
            transcript = Transcript(
                meeting_id=metadata.meeting_id,
                text=transcription_result['text'],
                confidence=transcription_result['confidence'],
                language=transcription_result.get('language', 'en'),
                duration_seconds=transcription_result.get('duration_seconds'),
                created_at=datetime.utcnow()
            )
            
            logger.info(
                f"Transcription completed: {len(transcript.text)} chars, "
                f"confidence: {transcript.confidence}"
            )
            
            # Step 2: Summarize (if requested)
            summary = None
            if auto_summarize:
                logger.info("Step 2/2: Generating summary and extracting action items")
                summary = self._generate_summary(transcript, metadata)
                logger.info(
                    f"Summary generated: {len(summary.action_items)} action items, "
                    f"{len(summary.decisions)} decisions"
                )
            else:
                logger.info("Step 2/2: Skipped (auto_summarize=False)")
            
            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            logger.info(
                f"Meeting processing completed in {processing_time:.2f}s "
                f"(target: <300s per spec.md)"
            )
            
            return transcript, summary
            
        except Exception as e:
            logger.error(f"Failed to process meeting {metadata.meeting_id}: {str(e)}")
            raise
    
    def _generate_summary(
        self, 
        transcript: Transcript, 
        metadata: MeetingMetadata
    ) -> Summary:
        """
        Generate a comprehensive summary from a transcript.
        
        Args:
            transcript: The meeting transcript
            metadata: Meeting metadata
            
        Returns:
            Summary object with extracted information
        """
        # Use summarizer to extract all components
        summary_data = self.summarizer.summarize(
            transcript.text, 
            transcript.meeting_id
        )
        
        # Convert action items to model objects
        action_items = [
            ActionItem(
                text=item['text'],
                assignee=item.get('assignee'),
                confidence=item['confidence'],
                needs_clarification=item.get('needs_clarification', False)
            )
            for item in summary_data['action_items']
        ]
        
        # Convert decisions to model objects
        decisions = [
            Decision(
                decision=dec['decision'],
                context=dec['context'],
                confidence=dec['confidence'],
                timestamp=dec.get('timestamp')
            )
            for dec in summary_data['decisions']
        ]
        
        # Create summary object
        summary = Summary(
            meeting_id=transcript.meeting_id,
            summary_text=summary_data['summary_text'],
            key_points=summary_data['key_points'],
            action_items=action_items,
            decisions=decisions,
            generated_at=datetime.utcnow()
        )
        
        return summary
    
    def transcribe_only(self, audio_file_path: str, meeting_id: str) -> Transcript:
        """
        Transcribe audio without generating summary.
        
        Useful when summary generation should be deferred or done separately.
        
        Args:
            audio_file_path: Path to audio file
            meeting_id: Meeting identifier
            
        Returns:
            Transcript object
        """
        logger.info(f"Transcribing audio only for meeting {meeting_id}")
        
        transcription_result = self.transcriber.transcribe_audio(
            audio_file_path,
            meeting_id
        )
        
        transcript = Transcript(
            meeting_id=meeting_id,
            text=transcription_result['text'],
            confidence=transcription_result['confidence'],
            language=transcription_result.get('language', 'en'),
            duration_seconds=transcription_result.get('duration_seconds'),
            created_at=datetime.utcnow()
        )
        
        return transcript
    
    def summarize_transcript(self, transcript: Transcript) -> Summary:
        """
        Generate summary from an existing transcript.
        
        Useful when transcription was done separately from summarization.
        
        Args:
            transcript: Existing transcript object
            
        Returns:
            Summary object
        """
        logger.info(f"Summarizing transcript for meeting {transcript.meeting_id}")
        
        summary_data = self.summarizer.summarize(
            transcript.text,
            transcript.meeting_id
        )
        
        # Convert to model objects
        action_items = [
            ActionItem(
                text=item['text'],
                assignee=item.get('assignee'),
                confidence=item['confidence'],
                needs_clarification=item.get('needs_clarification', False)
            )
            for item in summary_data['action_items']
        ]
        
        decisions = [
            Decision(
                decision=dec['decision'],
                context=dec['context'],
                confidence=dec['confidence'],
                timestamp=dec.get('timestamp')
            )
            for dec in summary_data['decisions']
        ]
        
        summary = Summary(
            meeting_id=transcript.meeting_id,
            summary_text=summary_data['summary_text'],
            key_points=summary_data['key_points'],
            action_items=action_items,
            decisions=decisions,
            generated_at=datetime.utcnow()
        )
        
        return summary
