"""Tests for meeting transcription and summarization."""
import pytest
from sparkfleet_api.transcription import (
    MeetingProcessor,
    TranscriptionService,
    SummarizationService,
    ActionItem,
    MeetingSummary
)


class TestTranscriptionService:
    """Tests for the TranscriptionService."""

    def test_transcribe_audio_returns_text(self):
        """Test that transcribe_audio returns transcript text."""
        service = TranscriptionService()
        result = service.transcribe_audio(
            audio_file_path="/fake/path/audio.mp3",
            meeting_id="meeting-123"
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "meeting-123" in result.lower()

    def test_validate_audio_file(self):
        """Test audio file validation."""
        service = TranscriptionService()
        result = service.validate_audio_file("/fake/path/audio.mp3")
        assert isinstance(result, bool)


class TestSummarizationService:
    """Tests for the SummarizationService."""

    def test_summarize_transcript_returns_summary(self):
        """Test that summarize_transcript returns a MeetingSummary."""
        service = SummarizationService()
        transcript = """
        Participant A: Let's discuss the Q4 roadmap priorities.
        Participant B: We need to focus on the API integration features.
        Participant A: Agreed. Can you take ownership of the GitHub integration?
        Participant B: Yes, I'll have that done by next Friday.
        """
        
        result = service.summarize_transcript(transcript)
        
        assert isinstance(result, MeetingSummary)
        assert isinstance(result.key_points, list)
        assert isinstance(result.decisions, list)
        assert isinstance(result.action_items, list)

    def test_extract_action_items(self):
        """Test action item extraction."""
        service = SummarizationService()
        transcript = """
        Participant A: I'll complete the documentation by Friday.
        Participant B: I can review the pull request tomorrow.
        """
        
        result = service.summarize_transcript(transcript)
        
        assert len(result.action_items) > 0
        for item in result.action_items:
            assert isinstance(item, ActionItem)
            assert isinstance(item.description, str)
            assert 0.0 <= item.confidence_score <= 1.0

    def test_extract_key_points(self):
        """Test key point extraction."""
        service = SummarizationService()
        transcript = """
        Participant A: We need to focus on security improvements.
        Participant B: Let's prioritize the authentication feature.
        """
        
        result = service.summarize_transcript(transcript)
        
        assert len(result.key_points) > 0
        assert all(isinstance(point, str) for point in result.key_points)


class TestMeetingProcessor:
    """Tests for the MeetingProcessor."""

    def test_process_meeting_returns_processed_meeting(self):
        """Test that process_meeting returns a ProcessedMeeting object."""
        processor = MeetingProcessor()
        
        result = processor.process_meeting(
            meeting_id="meeting-456",
            audio_file_path="/fake/path/audio.mp3",
            participants=["Alice", "Bob"],
            duration_minutes=30
        )
        
        assert result.meeting_id == "meeting-456"
        assert result.transcript is not None
        assert result.summary is not None
        assert result.transcript.meeting_id == "meeting-456"
        assert result.transcript.participants == ["Alice", "Bob"]
        assert result.transcript.duration_minutes == 30

    def test_process_meeting_extracts_action_items(self):
        """Test that processing extracts action items."""
        processor = MeetingProcessor()
        
        result = processor.process_meeting(
            meeting_id="meeting-789",
            audio_file_path="/fake/path/audio.mp3"
        )
        
        # The stub transcription includes action items
        assert isinstance(result.summary.action_items, list)

    def test_process_meeting_on_call_end(self):
        """Test the call end event handler."""
        processor = MeetingProcessor()
        
        result = processor.process_meeting_on_call_end(
            meeting_id="meeting-call-end",
            audio_file_path="/fake/path/audio.mp3",
            participants=["User1", "User2"]
        )
        
        assert result.meeting_id == "meeting-call-end"
        assert result.transcript is not None
        assert result.summary is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
