"""
Automated Transcription & Summarization Module

Handles transcription of meeting audio and summarization of key points.
Extracts action items from meeting content.

Spec Reference: Functional Requirement #1
"""

from .transcriber import Transcriber
from .summarizer import Summarizer
from .meeting_processor import MeetingProcessor

__all__ = ['Transcriber', 'Summarizer', 'MeetingProcessor']
