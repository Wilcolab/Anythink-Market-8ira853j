"""
Unit tests for the Transcriber class
"""

import pytest
import tempfile
import os
from pathlib import Path
from sparkfleet_predictive_maintenance_api.transcription import Transcriber


class TestTranscriber:
    """Test cases for audio transcription functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.transcriber = Transcriber()
    
    def test_transcriber_initialization(self):
        """Test that transcriber initializes correctly."""
        assert self.transcriber is not None
        assert self.transcriber.api_key is None
    
    def test_transcriber_with_api_key(self):
        """Test transcriber initialization with API key."""
        transcriber = Transcriber(api_key="test_key")
        assert transcriber.api_key == "test_key"
    
    def test_transcribe_audio_with_valid_file(self):
        """Test transcription with a valid audio file."""
        # Create a temporary audio file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(b'fake audio content')
            temp_file = f.name
        
        try:
            result = self.transcriber.transcribe_audio(temp_file, meeting_id="test_meeting")
            
            # Verify result structure
            assert 'text' in result
            assert 'confidence' in result
            assert 'language' in result
            assert 'duration_seconds' in result
            
            # Verify result values
            assert isinstance(result['text'], str)
            assert len(result['text']) > 0
            assert 0.0 <= result['confidence'] <= 1.0
            assert result['language'] == 'en'
            
        finally:
            # Clean up
            os.unlink(temp_file)
    
    def test_transcribe_audio_file_not_found(self):
        """Test transcription with non-existent file."""
        with pytest.raises(ValueError, match="Audio file not found"):
            self.transcriber.transcribe_audio("/nonexistent/file.mp3")
    
    def test_transcribe_audio_unsupported_format(self):
        """Test transcription with unsupported file format."""
        # Create a temporary file with unsupported extension
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b'not audio')
            temp_file = f.name
        
        try:
            with pytest.raises(ValueError, match="Unsupported audio format"):
                self.transcriber.transcribe_audio(temp_file)
        finally:
            os.unlink(temp_file)
    
    def test_transcribe_audio_supported_formats(self):
        """Test that all supported formats are accepted."""
        supported_formats = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
        
        for fmt in supported_formats:
            with tempfile.NamedTemporaryFile(suffix=fmt, delete=False) as f:
                f.write(b'fake audio')
                temp_file = f.name
            
            try:
                result = self.transcriber.transcribe_audio(temp_file)
                assert result is not None
                assert 'text' in result
            finally:
                os.unlink(temp_file)
    
    def test_transcribe_stream_not_implemented(self):
        """Test that streaming transcription raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            self.transcriber.transcribe_stream(None)
    
    def test_sample_transcript_generation(self):
        """Test that sample transcript contains expected elements."""
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(b'audio content')
            temp_file = f.name
        
        try:
            result = self.transcriber.transcribe_audio(temp_file, meeting_id="test")
            transcript = result['text']
            
            # Verify transcript contains meeting-like content
            assert 'meeting' in transcript.lower()
            assert len(transcript) > 100  # Should be substantial
            
        finally:
            os.unlink(temp_file)
