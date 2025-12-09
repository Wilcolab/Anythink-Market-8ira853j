#!/usr/bin/env python3
"""
Demo script to test the automatic meeting transcription and summarization feature.

This script demonstrates the complete flow of processing a meeting after it ends.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sparkfleet_api.transcription.models import Meeting, MeetingPlatform, MeetingStatus
from sparkfleet_api.transcription.meeting_processor import MeetingProcessor
from sparkfleet_api.transcription.api_example import TranscriptionAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def demo_basic_flow():
    """Demonstrate the basic meeting processing flow."""
    print("\n" + "="*80)
    print("DEMO: Automatic Meeting Transcription and Summarization")
    print("="*80 + "\n")
    
    # Create a meeting that has ended
    meeting = Meeting(
        id="demo-meeting-001",
        title="Q4 Product Planning Meeting",
        platform=MeetingPlatform.ZOOM,
        start_time=datetime(2024, 1, 15, 10, 0, 0),
        end_time=datetime(2024, 1, 15, 11, 0, 0),
        status=MeetingStatus.ENDED,
        participants=["alice@company.com", "bob@company.com", "charlie@company.com"],
        audio_url="https://zoom.us/rec/play/demo123"
    )
    
    print(f"📅 Meeting: {meeting.title}")
    print(f"🆔 ID: {meeting.id}")
    print(f"🕐 Duration: {meeting.start_time} - {meeting.end_time}")
    print(f"👥 Participants: {', '.join(meeting.participants)}")
    print(f"📊 Status: {meeting.status.value}")
    print(f"🎥 Platform: {meeting.platform.value}")
    print("\n" + "-"*80 + "\n")
    
    # Process the meeting
    print("⚙️  Processing meeting (transcription + summarization)...")
    processor = MeetingProcessor()
    transcription, summary = processor.process_meeting_end(meeting)
    
    if not transcription or not summary:
        print("❌ Failed to process meeting")
        return
    
    print("✅ Meeting processed successfully!\n")
    print("-"*80 + "\n")
    
    # Display transcription
    print("📝 TRANSCRIPTION:")
    print(f"   Length: {len(transcription.text)} characters")
    print(f"   Confidence: {transcription.confidence_score:.1%}")
    print(f"   Language: {transcription.language}")
    print(f"\n   Text Preview:")
    preview = transcription.text.strip()[:200]
    print(f"   {preview}...\n")
    print("-"*80 + "\n")
    
    # Display summary
    print("📋 SUMMARY:\n")
    
    if summary.key_points:
        print("🔑 Key Discussion Points:")
        for i, point in enumerate(summary.key_points, 1):
            print(f"   {i}. {point.strip()}")
        print()
    
    if summary.decisions:
        print("✓ Decisions Made:")
        for i, decision in enumerate(summary.decisions, 1):
            print(f"   {i}. {decision.strip()}")
        print()
    
    if summary.action_items:
        print("⚡ Action Items:")
        for i, item in enumerate(summary.action_items, 1):
            assignee = f" [{item.assignee}]" if item.assignee else ""
            confidence = f" (confidence: {item.confidence_score:.0%})"
            print(f"   {i}. {item.description.strip()}{assignee}{confidence}")
        print()
    
    print("-"*80 + "\n")
    print("✨ Demo completed successfully!")
    print("\n")


def demo_webhook_integration():
    """Demonstrate webhook integration."""
    print("\n" + "="*80)
    print("DEMO: Webhook Integration")
    print("="*80 + "\n")
    
    api = TranscriptionAPI()
    
    # Simulate a webhook from Zoom
    webhook_payload = {
        "platform": "zoom",
        "meeting_id": "zoom-123456",
        "topic": "Customer Feedback Review",
        "start_time": "2024-01-15T14:00:00",
        "participants": ["sarah@company.com", "john@company.com"],
        "recording_url": "https://zoom.us/rec/play/webhook-demo"
    }
    
    print("📨 Received webhook from Zoom:")
    print(f"   Meeting ID: {webhook_payload['meeting_id']}")
    print(f"   Topic: {webhook_payload['topic']}")
    print(f"   Participants: {', '.join(webhook_payload['participants'])}")
    print("\n⚙️  Processing webhook...\n")
    
    result = api.webhook_meeting_ended(webhook_payload)
    
    if result.get("status") == "success":
        print("✅ Webhook processed successfully!")
        print(f"\n📋 Summary Preview:")
        summary = result.get("summary", {})
        print(f"   - {len(summary.get('key_points', []))} key points")
        print(f"   - {len(summary.get('decisions', []))} decisions")
        print(f"   - {len(summary.get('action_items', []))} action items")
    else:
        print(f"❌ Webhook processing failed: {result.get('message')}")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    # Run demos
    demo_basic_flow()
    demo_webhook_integration()
