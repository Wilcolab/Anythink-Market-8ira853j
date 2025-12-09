#!/usr/bin/env python
"""
Demo script showing automatic meeting transcription and summarization.

This demonstrates the key feature: meetings can be transcribed and summarized
automatically after call ends.
"""
from sparkfleet_api.transcription import MeetingProcessor
import json


def main():
    """Run the demo."""
    print("=" * 80)
    print("SparkFleet Meeting Assistant - Automatic Transcription Demo")
    print("=" * 80)
    print()
    
    # Initialize the meeting processor
    processor = MeetingProcessor()
    
    # Simulate a meeting ending and being processed
    print("📞 Meeting has ended. Starting automatic processing...")
    print()
    
    # Process the meeting (in production, this would be triggered by Zoom/GMeet webhook)
    result = processor.process_meeting_on_call_end(
        meeting_id="demo-sales-call-20231209",
        audio_file_path="/recordings/sales_call.mp3",
        participants=["Sarah (Sales)", "John (Customer)", "Mike (PM)"],
        duration_minutes=35
    )
    
    print("✅ Processing complete!")
    print()
    print("-" * 80)
    print("MEETING TRANSCRIPT")
    print("-" * 80)
    print(f"Meeting ID: {result.transcript.meeting_id}")
    print(f"Duration: {result.transcript.duration_minutes} minutes")
    print(f"Participants: {', '.join(result.transcript.participants)}")
    print()
    print("Transcript:")
    print(result.transcript.transcript_text)
    print()
    
    print("-" * 80)
    print("MEETING SUMMARY")
    print("-" * 80)
    print()
    
    print("📝 KEY POINTS:")
    for i, point in enumerate(result.summary.key_points, 1):
        print(f"  {i}. {point}")
    print()
    
    print("✅ DECISIONS MADE:")
    for i, decision in enumerate(result.summary.decisions, 1):
        print(f"  {i}. {decision}")
    print()
    
    print("🎯 ACTION ITEMS:")
    if result.summary.action_items:
        for i, item in enumerate(result.summary.action_items, 1):
            print(f"  {i}. {item.description}")
            print(f"     Assignee: {item.assignee or 'Not specified'}")
            print(f"     Confidence: {item.confidence_score:.0%}")
            if item.needs_clarification:
                print(f"     ⚠️  Needs clarification")
            print()
    else:
        print("  No action items detected")
    print()
    
    print("-" * 80)
    print("📊 SUMMARY STATISTICS")
    print("-" * 80)
    print(f"Key Points Extracted: {len(result.summary.key_points)}")
    print(f"Decisions Captured: {len(result.summary.decisions)}")
    print(f"Action Items Found: {len(result.summary.action_items)}")
    print()
    
    print("=" * 80)
    print("✨ Meeting processed successfully!")
    print("The summary and action items are now available in SparkFleet UI")
    print("=" * 80)


if __name__ == "__main__":
    main()
