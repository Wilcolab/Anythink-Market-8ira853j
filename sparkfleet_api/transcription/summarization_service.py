"""Service for summarizing meeting transcriptions."""

import logging
import re
from typing import List, Optional
from datetime import datetime

from .models import Transcription, Summary, ActionItem

logger = logging.getLogger(__name__)


class SummarizationService:
    """
    Service for summarizing meeting transcriptions and extracting action items.
    
    This is a stub implementation that can be extended to integrate with
    actual AI/LLM APIs like GPT, Claude, or custom models.
    """
    
    def __init__(self):
        """Initialize the summarization service."""
        self.model = "gpt-4"  # Default model for summarization
        
    def summarize_meeting(self, transcription: Transcription) -> Optional[Summary]:
        """
        Generate a summary from meeting transcription.
        
        Args:
            transcription: Transcription object with meeting text
            
        Returns:
            Summary object with key points, decisions, and action items
        """
        if not transcription or not transcription.text:
            logger.error("No transcription text provided")
            return None
            
        try:
            logger.info(f"Starting summarization for meeting {transcription.meeting_id}")
            
            # Extract key points
            key_points = self._extract_key_points(transcription.text)
            
            # Extract decisions
            decisions = self._extract_decisions(transcription.text)
            
            # Extract action items
            action_items = self._extract_action_items(transcription.text)
            
            # Generate overall summary
            summary_text = self._generate_summary_text(key_points, decisions, action_items)
            
            summary = Summary(
                meeting_id=transcription.meeting_id,
                key_points=key_points,
                decisions=decisions,
                action_items=action_items,
                timestamp=datetime.utcnow(),
                summary_text=summary_text
            )
            
            logger.info(f"Successfully summarized meeting {transcription.meeting_id}")
            return summary
            
        except Exception as e:
            logger.error(f"Error summarizing meeting {transcription.meeting_id}: {str(e)}")
            return None
    
    def _extract_key_points(self, text: str) -> List[str]:
        """
        Extract key discussion points from transcription.
        
        Args:
            text: Transcription text
            
        Returns:
            List of key points
        """
        # TODO: Implement actual NLP-based key point extraction
        # For now, use simple sentence detection
        key_points = []
        
        # Look for sentences that indicate topics or discussions
        sentences = text.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in 
                   ['discussed', 'talked about', 'mentioned', 'focus on']):
                if sentence and len(sentence) > 20:
                    key_points.append(sentence)
        
        return key_points[:5]  # Limit to top 5 key points
    
    def _extract_decisions(self, text: str) -> List[str]:
        """
        Extract decisions made during the meeting.
        
        Args:
            text: Transcription text
            
        Returns:
            List of decisions
        """
        # TODO: Implement actual decision detection using NLP
        decisions = []
        
        # Look for sentences indicating decisions
        sentences = text.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in 
                   ['decided', 'agreed', 'determined', 'concluded', 'prioritize']):
                if sentence and len(sentence) > 20:
                    decisions.append(sentence)
        
        return decisions
    
    def _extract_action_items(self, text: str) -> List[ActionItem]:
        """
        Extract action items and commitments from transcription.
        
        Args:
            text: Transcription text
            
        Returns:
            List of ActionItem objects
        """
        # TODO: Implement actual action item detection using NLP
        action_items = []
        
        # Pattern to match "Person said/mentioned/committed to do something"
        sentences = text.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            
            # Look for commitment patterns
            if any(keyword in sentence.lower() for keyword in 
                   ['will', 'would', 'committed', 'agreed to', 'need to']):
                
                # Try to extract assignee (person's name before the commitment)
                assignee = None
                words = sentence.split()
                for i, word in enumerate(words):
                    if word[0].isupper() and len(word) > 2 and word.isalpha():
                        if i < len(words) - 1 and any(commit in words[i+1:i+3] for commit in ['will', 'would', 'committed']):
                            assignee = word
                            break
                
                if len(sentence) > 20:
                    action_item = ActionItem(
                        description=sentence,
                        assignee=assignee,
                        confidence_score=0.85,
                        source_segment=sentence
                    )
                    action_items.append(action_item)
        
        return action_items
    
    def _generate_summary_text(self, key_points: List[str], 
                               decisions: List[str], 
                               action_items: List[ActionItem]) -> str:
        """
        Generate a coherent summary text.
        
        Args:
            key_points: List of key discussion points
            decisions: List of decisions made
            action_items: List of action items
            
        Returns:
            Summary text
        """
        summary_parts = []
        
        if key_points:
            summary_parts.append("**Key Discussion Points:**")
            for i, point in enumerate(key_points, 1):
                summary_parts.append(f"{i}. {point}")
        
        if decisions:
            summary_parts.append("\n**Decisions Made:**")
            for i, decision in enumerate(decisions, 1):
                summary_parts.append(f"{i}. {decision}")
        
        if action_items:
            summary_parts.append("\n**Action Items:**")
            for i, item in enumerate(action_items, 1):
                assignee_text = f" ({item.assignee})" if item.assignee else ""
                summary_parts.append(f"{i}. {item.description}{assignee_text}")
        
        return "\n".join(summary_parts)
