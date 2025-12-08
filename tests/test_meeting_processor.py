"""
Integration tests for the MeetingProcessor class
"""

import pytest
import tempfile
import os
from datetime import datetime
from sparkfleet_predictive_maintenance_api.transcription import MeetingProcessor
from sparkfleet_predictive_maintenance_api.models import MeetingMetadata


class TestMeetingProcessor:
    """Test cases for the meeting processing pipeline."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = MeetingProcessor()
        self.sample_metadata = MeetingMetadata(
            meeting_id="test_meeting_001",
            title="Test Project Meeting",
            participants=["Alice", "Bob", "Charlie"],
            start_time=datetime.utcnow(),
            platform="zoom"
        )
    
    def test_processor_initialization(self):
        """Test that processor initializes correctly."""
        assert self.processor is not None
        assert self.processor.transcriber is not None
        assert self.processor.summarizer is not None
    
    def test_process_meeting_end_to_end(self):
        """Test full meeting processing pipeline."""
        # Create a temporary audio file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(b'fake audio content for testing')
            temp_file = f.name
        
        try:
            # Process the meeting
            transcript, summary = self.processor.process_meeting(
                audio_file_path=temp_file,
                metadata=self.sample_metadata,
                auto_summarize=True
            )
            
            # Verify transcript
            assert transcript is not None
            assert transcript.meeting_id == "test_meeting_001"
            assert len(transcript.text) > 0
            assert 0.0 <= transcript.confidence <= 1.0
            
            # Verify summary
            assert summary is not None
            assert summary.meeting_id == "test_meeting_001"
            assert len(summary.summary_text) > 0
            assert isinstance(summary.action_items, list)
            assert isinstance(summary.decisions, list)
            assert isinstance(summary.key_points, list)
            
        finally:
            os.unlink(temp_file)
    
    def test_process_meeting_without_summary(self):
        """Test processing without automatic summarization."""
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(b'audio content')
            temp_file = f.name
        
        try:
            transcript, summary = self.processor.process_meeting(
                audio_file_path=temp_file,
                metadata=self.sample_metadata,
                auto_summarize=False
            )
            
            assert transcript is not None
            assert summary is None
            
        finally:
            os.unlink(temp_file)
    
    def test_process_meeting_invalid_file(self):
        """Test processing with invalid audio file."""
        with pytest.raises(ValueError):
            self.processor.process_meeting(
                audio_file_path="/nonexistent/file.mp3",
                metadata=self.sample_metadata,
                auto_summarize=True
            )
    
    def test_transcribe_only(self):
        """Test transcription without summarization."""
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(b'audio data')
            temp_file = f.name
        
        try:
            transcript = self.processor.transcribe_only(
                audio_file_path=temp_file,
                meeting_id="transcribe_only_test"
            )
            
            assert transcript is not None
            assert transcript.meeting_id == "transcribe_only_test"
            assert len(transcript.text) > 0
            
        finally:
            os.unlink(temp_file)
    
    def test_summarize_transcript(self):
        """Test summarization of existing transcript."""
        # First, get a transcript
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(b'audio')
            temp_file = f.name
        
        try:
            transcript = self.processor.transcribe_only(temp_file, "test_summarize")
            
            # Now summarize it
            summary = self.processor.summarize_transcript(transcript)
            
            assert summary is not None
            assert summary.meeting_id == transcript.meeting_id
            assert len(summary.summary_text) > 0
            assert isinstance(summary.action_items, list)
            assert isinstance(summary.decisions, list)
            
        finally:
            os.unlink(temp_file)
    
    def test_action_items_in_summary(self):
        """Test that action items are properly extracted in full pipeline."""
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(b'meeting audio')
            temp_file = f.name
        
        try:
            _, summary = self.processor.process_meeting(
                audio_file_path=temp_file,
                metadata=self.sample_metadata,
                auto_summarize=True
            )
            
            # The sample transcript includes action items
            assert summary is not None
            assert len(summary.action_items) > 0
            
            # Verify action item structure
            for item in summary.action_items:
                assert hasattr(item, 'text')
                assert hasattr(item, 'confidence')
                assert 0.0 <= item.confidence <= 1.0
            
        finally:
            os.unlink(temp_file)
    
    def test_decisions_in_summary(self):
        """Test that decisions are properly extracted in full pipeline."""
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(b'meeting with decisions')
            temp_file = f.name
        
        try:
            _, summary = self.processor.process_meeting(
                audio_file_path=temp_file,
                metadata=self.sample_metadata,
                auto_summarize=True
            )
            
            # The sample transcript includes decisions
            assert summary is not None
            assert len(summary.decisions) > 0
            
            # Verify decision structure
            for decision in summary.decisions:
                assert hasattr(decision, 'decision')
                assert hasattr(decision, 'confidence')
                assert 0.0 <= decision.confidence <= 1.0
            
        finally:
            os.unlink(temp_file)
    
    def test_processing_time_reasonable(self):
        """Test that processing completes in reasonable time."""
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(b'audio for timing test')
            temp_file = f.name
        
        try:
            start = datetime.utcnow()
            
            self.processor.process_meeting(
                audio_file_path=temp_file,
                metadata=self.sample_metadata,
                auto_summarize=True
            )
            
            elapsed = (datetime.utcnow() - start).total_seconds()
            
            # Should complete well under the 5-minute spec requirement
            # For this mock implementation, should be nearly instant
            assert elapsed < 5.0  # 5 seconds should be plenty for mock
            
        finally:
            os.unlink(temp_file)
