"""
Meeting summarization module

Generates summaries of meeting transcripts and extracts action items.
"""

import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class Summarizer:
    """
    Generates summaries and extracts action items from meeting transcripts.
    
    This implementation uses pattern matching and text analysis.
    In production, this would integrate with LLM services like:
    - OpenAI GPT
    - Anthropic Claude
    - Azure OpenAI
    - Local models via LangChain
    """
    
    # Patterns for detecting action items
    ACTION_PATTERNS = [
        r"(?:you said you would|you'll|you will|you're going to)\s+(.+?)(?:\.|;|$)",
        r"(?:I'll|I will|I'm going to)\s+(.+?)(?:\.|;|$)",
        r"(?:we'll|we will|we're going to)\s+(.+?)(?:\.|;|$)",
        r"(?:should|need to|must|has to)\s+(.+?)(?:\.|;|$)",
    ]
    
    # Patterns for detecting decisions
    DECISION_PATTERNS = [
        r"(?:we've decided|we decided|decision|let's proceed|let's go with)\s+(.+?)(?:\.|;|$)",
        r"(?:agreed to|agreement|consensus)\s+(.+?)(?:\.|;|$)",
    ]
    
    def __init__(self):
        """Initialize summarizer."""
        logger.info("Summarizer initialized")
    
    def summarize(self, transcript: str, meeting_id: str = None) -> dict:
        """
        Generate summary from meeting transcript.
        
        Uses text analysis to extract key information. In production,
        this would use LLM APIs for more sophisticated summarization.
        
        Args:
            transcript: Full meeting transcript text
            meeting_id: Optional meeting identifier
            
        Returns:
            dict with 'summary_text', 'key_points', 'decisions', 'action_items' keys
        """
        logger.info(f"Generating summary for transcript ({len(transcript)} chars)")
        
        # Extract components
        action_items = self.extract_action_items(transcript)
        decisions = self.extract_decisions(transcript)
        key_points = self._extract_key_points(transcript)
        summary_text = self._generate_summary_text(transcript, key_points, decisions, action_items)
        
        result = {
            'summary_text': summary_text,
            'key_points': key_points,
            'decisions': decisions,
            'action_items': action_items
        }
        
        logger.info(
            f"Summary generated: {len(key_points)} key points, "
            f"{len(decisions)} decisions, {len(action_items)} action items"
        )
        
        return result
    
    def extract_action_items(self, transcript: str) -> List[Dict[str, Any]]:
        """
        Extract action items from transcript.
        
        Detects patterns like "you said you would...", "I'll...", "we'll...", etc.
        
        Args:
            transcript: Full meeting transcript text
            
        Returns:
            list of dicts with 'text', 'assignee', 'confidence', 'needs_clarification' keys
        """
        action_items = []
        lines = transcript.split('\n')
        
        for line in lines:
            # Try to extract speaker name
            speaker_match = re.match(r'\[[\d:]+\]\s*([^:]+):', line)
            speaker = speaker_match.group(1).strip() if speaker_match else None
            
            # Check each action pattern
            for pattern in self.ACTION_PATTERNS:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    action_text = match.group(1).strip()
                    
                    # Skip very short or generic matches
                    if len(action_text) < 10:
                        continue
                    
                    # Determine assignee based on pattern
                    assignee = None
                    confidence = 0.85  # Default confidence
                    needs_clarification = False
                    
                    if re.search(r"you said you would", line, re.IGNORECASE):
                        # High confidence for explicit commitments
                        confidence = 0.95
                        # Try to determine who "you" refers to
                        if speaker and speaker.lower() not in ['moderator', 'host']:
                            # Speaker is asking someone else
                            assignee = "to be determined"
                            needs_clarification = True
                    elif re.search(r"I'll|I will|I'm going to", line, re.IGNORECASE):
                        assignee = speaker
                        confidence = 0.90
                    elif re.search(r"we'll|we will|we're going to", line, re.IGNORECASE):
                        assignee = "team"
                        confidence = 0.80
                    else:
                        # Lower confidence for should/need/must patterns
                        confidence = 0.70
                        needs_clarification = True
                    
                    action_items.append({
                        'text': action_text,
                        'assignee': assignee,
                        'confidence': confidence,
                        'needs_clarification': needs_clarification
                    })
        
        # Remove duplicates (keeping highest confidence)
        unique_items = {}
        for item in action_items:
            key = item['text'].lower()
            if key not in unique_items or item['confidence'] > unique_items[key]['confidence']:
                unique_items[key] = item
        
        return list(unique_items.values())
    
    def extract_decisions(self, transcript: str) -> List[Dict[str, Any]]:
        """
        Extract key decisions from transcript.
        
        Identifies statements indicating decisions were made.
        
        Args:
            transcript: Full meeting transcript text
            
        Returns:
            list of dicts with 'decision', 'context', 'confidence', 'timestamp' keys
        """
        decisions = []
        lines = transcript.split('\n')
        
        for line in lines:
            # Extract timestamp if present
            timestamp_match = re.match(r'\[([^\]]+)\]', line)
            timestamp = timestamp_match.group(1) if timestamp_match else None
            
            # Check each decision pattern
            for pattern in self.DECISION_PATTERNS:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    decision_text = match.group(1).strip()
                    
                    # Skip very short matches
                    if len(decision_text) < 10:
                        continue
                    
                    # Get surrounding context (current line)
                    context = line.strip()
                    
                    # Higher confidence for explicit decision keywords
                    confidence = 0.90 if re.search(r"decided|decision", line, re.IGNORECASE) else 0.80
                    
                    decisions.append({
                        'decision': decision_text,
                        'context': context,
                        'confidence': confidence,
                        'timestamp': timestamp
                    })
        
        # Remove duplicates
        unique_decisions = {}
        for decision in decisions:
            key = decision['decision'].lower()
            if key not in unique_decisions or decision['confidence'] > unique_decisions[key]['confidence']:
                unique_decisions[key] = decision
        
        return list(unique_decisions.values())
    
    def _extract_key_points(self, transcript: str) -> List[str]:
        """
        Extract key discussion points from transcript.
        
        Args:
            transcript: Full meeting transcript
            
        Returns:
            List of key points
        """
        key_points = []
        lines = transcript.split('\n')
        
        # Look for topic introduction patterns
        topic_patterns = [
            r"(?:let's|we need to|next,? we)\s+(.+?)(?:\.|$)",
            r"(?:discuss|review|talk about)\s+(.+?)(?:\.|$)",
            r"(?:update on|status of)\s+(.+?)(?:\.|$)",
        ]
        
        for line in lines:
            for pattern in topic_patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    point = match.group(1).strip()
                    if len(point) > 15 and point not in key_points:
                        key_points.append(point)
        
        # Limit to most relevant points
        return key_points[:5]
    
    def _generate_summary_text(
        self, 
        transcript: str, 
        key_points: List[str],
        decisions: List[Dict],
        action_items: List[Dict]
    ) -> str:
        """
        Generate overall summary text.
        
        Args:
            transcript: Full transcript
            key_points: Extracted key points
            decisions: Extracted decisions
            action_items: Extracted action items
            
        Returns:
            Summary text
        """
        # Count approximate participants
        speakers = set()
        for line in transcript.split('\n'):
            speaker_match = re.match(r'\[[\d:]+\]\s*([^:]+):', line)
            if speaker_match:
                speakers.add(speaker_match.group(1).strip())
        
        summary_parts = []
        
        # Opening
        summary_parts.append(
            f"Meeting attended by {len(speakers)} participant(s). "
        )
        
        # Key topics
        if key_points:
            summary_parts.append(
                f"Key topics discussed included: {', '.join(key_points[:3])}. "
            )
        
        # Decisions
        if decisions:
            summary_parts.append(
                f"The team made {len(decisions)} key decision(s). "
            )
        
        # Action items
        if action_items:
            summary_parts.append(
                f"A total of {len(action_items)} action item(s) were identified and assigned."
            )
        else:
            summary_parts.append("No specific action items were identified.")
        
        return ''.join(summary_parts)
