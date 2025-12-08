"""
Unit tests for the Summarizer class
"""

import pytest
from sparkfleet_predictive_maintenance_api.transcription import Summarizer


class TestSummarizer:
    """Test cases for meeting summarization functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.summarizer = Summarizer()
        self.sample_transcript = """
[00:00] Welcome everyone to the project meeting.

[00:15] Sarah, you said you would complete the API documentation by Friday.

[00:45] Sarah: Yes, I'll finish it by tomorrow.

[01:20] We've decided to prioritize the meeting transcription feature.

[02:00] John, you mentioned you would investigate transcription options.

[02:30] John: I looked into several options. I recommend we go with Whisper.

[03:15] Maria, you said you would draft the user requirements.

[03:45] Maria: I'll send the document today.

[04:30] We've decided to launch the MVP by end of Q4.

[05:00] John will set up the integration, Sarah will finish docs, Maria will complete requirements.
"""
    
    def test_summarizer_initialization(self):
        """Test that summarizer initializes correctly."""
        assert self.summarizer is not None
    
    def test_summarize_returns_expected_structure(self):
        """Test that summarize returns all expected fields."""
        result = self.summarizer.summarize(self.sample_transcript)
        
        assert 'summary_text' in result
        assert 'key_points' in result
        assert 'decisions' in result
        assert 'action_items' in result
        
        assert isinstance(result['summary_text'], str)
        assert isinstance(result['key_points'], list)
        assert isinstance(result['decisions'], list)
        assert isinstance(result['action_items'], list)
    
    def test_extract_action_items_basic(self):
        """Test extraction of basic action items."""
        action_items = self.summarizer.extract_action_items(self.sample_transcript)
        
        assert len(action_items) > 0
        
        # Verify structure of action items
        for item in action_items:
            assert 'text' in item
            assert 'assignee' in item
            assert 'confidence' in item
            assert 'needs_clarification' in item
            assert 0.0 <= item['confidence'] <= 1.0
    
    def test_extract_action_items_you_said_pattern(self):
        """Test extraction of 'you said you would' patterns."""
        transcript = "Sarah, you said you would complete the documentation by Friday."
        action_items = self.summarizer.extract_action_items(transcript)
        
        assert len(action_items) > 0
        # Should have high confidence for explicit commitments
        assert any(item['confidence'] >= 0.90 for item in action_items)
    
    def test_extract_action_items_ill_pattern(self):
        """Test extraction of 'I'll' patterns."""
        transcript = "[00:00] John: I'll finish the implementation by next week."
        action_items = self.summarizer.extract_action_items(transcript)
        
        assert len(action_items) > 0
        # Should extract assignee from speaker
        assert any(item['assignee'] == 'John' for item in action_items)
    
    def test_extract_action_items_well_pattern(self):
        """Test extraction of 'we'll' patterns."""
        transcript = "We'll review the proposal in the next meeting."
        action_items = self.summarizer.extract_action_items(transcript)
        
        assert len(action_items) > 0
        # Team assignments should have slightly lower confidence
        assert any(item['assignee'] == 'team' for item in action_items)
    
    def test_extract_decisions_basic(self):
        """Test extraction of basic decisions."""
        decisions = self.summarizer.extract_decisions(self.sample_transcript)
        
        assert len(decisions) > 0
        
        # Verify structure of decisions
        for decision in decisions:
            assert 'decision' in decision
            assert 'context' in decision
            assert 'confidence' in decision
            assert 'timestamp' in decision
            assert 0.0 <= decision['confidence'] <= 1.0
    
    def test_extract_decisions_decided_pattern(self):
        """Test extraction of 'decided' patterns."""
        transcript = "[01:00] We've decided to use Python for the backend."
        decisions = self.summarizer.extract_decisions(transcript)
        
        assert len(decisions) > 0
        # Should extract the decision
        assert any('Python' in dec['decision'] for dec in decisions)
    
    def test_extract_decisions_with_timestamp(self):
        """Test that timestamps are extracted with decisions."""
        transcript = "[01:30] We decided to launch in Q4."
        decisions = self.summarizer.extract_decisions(transcript)
        
        assert len(decisions) > 0
        # Should have timestamp
        assert any(dec['timestamp'] is not None for dec in decisions)
    
    def test_summarize_empty_transcript(self):
        """Test summarization with empty transcript."""
        result = self.summarizer.summarize("")
        
        assert result['summary_text'] != ""
        assert isinstance(result['action_items'], list)
        assert isinstance(result['decisions'], list)
    
    def test_summarize_no_action_items(self):
        """Test summarization when no action items present."""
        transcript = "We discussed the project status. Everything is on track."
        result = self.summarizer.summarize(transcript)
        
        # Should handle gracefully
        assert 'action_items' in result
        # Summary should mention no action items
        assert 'No specific action items' in result['summary_text'] or len(result['action_items']) == 0
    
    def test_action_item_deduplication(self):
        """Test that duplicate action items are removed."""
        transcript = """
        Sarah will complete the docs.
        Sarah: I will complete the docs.
        """
        action_items = self.summarizer.extract_action_items(transcript)
        
        # Should deduplicate similar items
        texts = [item['text'].lower() for item in action_items]
        # All texts should be unique
        assert len(texts) == len(set(texts))
    
    def test_decision_deduplication(self):
        """Test that duplicate decisions are removed."""
        transcript = """
        We decided to use Python.
        The team decided to use Python for the project.
        """
        decisions = self.summarizer.extract_decisions(transcript)
        
        # Should deduplicate similar decisions
        decision_texts = [dec['decision'].lower() for dec in decisions]
        assert len(decision_texts) == len(set(decision_texts))
    
    def test_confidence_scores_valid_range(self):
        """Test that all confidence scores are in valid range."""
        result = self.summarizer.summarize(self.sample_transcript)
        
        # Check action items
        for item in result['action_items']:
            assert 0.0 <= item['confidence'] <= 1.0
        
        # Check decisions
        for decision in result['decisions']:
            assert 0.0 <= decision['confidence'] <= 1.0
