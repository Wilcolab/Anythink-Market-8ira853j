"""Service for summarizing meeting transcripts and extracting action items."""
from typing import List
import re
import logging
from .models import MeetingSummary, ActionItem

logger = logging.getLogger(__name__)


class SummarizationService:
    """Service for summarizing meeting transcripts and extracting key information."""

    def __init__(self):
        """Initialize the summarization service."""
        logger.info("Initializing SummarizationService")

    def summarize_transcript(self, transcript_text: str) -> MeetingSummary:
        """
        Summarize a meeting transcript and extract key information.

        Args:
            transcript_text: The full meeting transcript

        Returns:
            MeetingSummary containing key points, decisions, and action items

        Note:
            In a production environment, this would use NLP models or LLMs
            like GPT, Claude, or custom-trained models for better accuracy.
        """
        logger.info("Summarizing meeting transcript")
        
        key_points = self._extract_key_points(transcript_text)
        decisions = self._extract_decisions(transcript_text)
        action_items = self._extract_action_items(transcript_text)
        
        return MeetingSummary(
            key_points=key_points,
            decisions=decisions,
            action_items=action_items
        )

    def _extract_key_points(self, transcript_text: str) -> List[str]:
        """
        Extract key discussion points from the transcript.

        Args:
            transcript_text: The full meeting transcript

        Returns:
            List of key points discussed
        """
        logger.debug("Extracting key points")
        
        # TODO: Use NLP/LLM for better extraction
        # Simple heuristic: look for sentences with key phrases
        key_phrases = [
            "need to", "focus on", "priority", "important",
            "discuss", "should", "must", "let's"
        ]
        
        key_points = []
        lines = transcript_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('['):
                continue
            
            # Remove speaker prefix
            if ':' in line:
                content = line.split(':', 1)[1].strip()
            else:
                content = line
            
            # Check if line contains key phrases
            if any(phrase in content.lower() for phrase in key_phrases):
                key_points.append(content)
        
        return key_points if key_points else ["Meeting discussion transcript available"]

    def _extract_decisions(self, transcript_text: str) -> List[str]:
        """
        Extract decisions made during the meeting.

        Args:
            transcript_text: The full meeting transcript

        Returns:
            List of decisions made
        """
        logger.debug("Extracting decisions")
        
        # TODO: Use NLP/LLM for better extraction
        # Simple heuristic: look for agreement/decision phrases
        decision_phrases = [
            "agreed", "decided", "will do", "confirmed",
            "approved", "let's go with", "we'll"
        ]
        
        decisions = []
        lines = transcript_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('['):
                continue
            
            # Remove speaker prefix
            if ':' in line:
                content = line.split(':', 1)[1].strip()
            else:
                content = line
            
            # Check if line contains decision phrases
            if any(phrase in content.lower() for phrase in decision_phrases):
                decisions.append(content)
        
        return decisions

    def _extract_action_items(self, transcript_text: str) -> List[ActionItem]:
        """
        Extract action items from the transcript.

        Args:
            transcript_text: The full meeting transcript

        Returns:
            List of ActionItem objects
        """
        logger.debug("Extracting action items")
        
        # TODO: Use NLP/LLM for better extraction
        # Simple heuristic: look for commitment phrases
        action_items = []
        lines = transcript_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('['):
                continue
            
            # Extract speaker and content
            speaker = None
            content = line
            if ':' in line:
                parts = line.split(':', 1)
                speaker = parts[0].strip()
                content = parts[1].strip()
            
            # Look for action patterns
            action_patterns = [
                r"i(?:'ll| will) (.+)",
                r"i can (.+)",
                r"i'll take (.+)",
                r"i'll (.+)",
                r"you said you (?:would|will) (.+)"
            ]
            
            for pattern in action_patterns:
                match = re.search(pattern, content.lower())
                if match:
                    action_description = match.group(1).strip()
                    # Capitalize first letter if not empty
                    if len(action_description) > 0:
                        action_description = action_description[0].upper() + action_description[1:]
                    
                    # Skip if description is too short or empty
                    if len(action_description) < 3:
                        continue
                    
                    # Calculate a simple confidence score
                    # Higher confidence for explicit commitments
                    confidence = 0.85 if "i'll" in content.lower() else 0.75
                    
                    action_items.append(ActionItem(
                        description=action_description,
                        assignee=speaker,
                        confidence_score=confidence,
                        needs_clarification=confidence < 0.8
                    ))
                    break
        
        return action_items
