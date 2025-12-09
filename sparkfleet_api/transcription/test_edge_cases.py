#!/usr/bin/env python3
"""
Test script for edge case handling in the transcription system.

This validates that the system properly handles missing or invalid data fields.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sparkfleet_api.transcription import (
    WebhookHandler, 
    TranscriptionAPI,
    MeetingProcessor,
    Meeting,
    MeetingPlatform,
    MeetingStatus
)
from datetime import datetime


def test_webhook_edge_cases():
    """Test webhook handler with various edge cases."""
    print("\n" + "="*80)
    print("Testing Webhook Handler Edge Cases")
    print("="*80 + "\n")
    
    handler = WebhookHandler()
    test_cases = [
        {
            "name": "Missing meeting_id",
            "data": {"topic": "Test"},
            "expected": "error"
        },
        {
            "name": "Empty meeting_id",
            "data": {"meeting_id": ""},
            "expected": "error"
        },
        {
            "name": "Whitespace-only meeting_id",
            "data": {"meeting_id": "   "},
            "expected": "error"
        },
        {
            "name": "None webhook data",
            "data": None,
            "expected": "error"
        },
        {
            "name": "Invalid participants type (string)",
            "data": {
                "meeting_id": "test-123",
                "participants": "not-a-list",
                "recording_url": "http://example.com/audio.mp3"
            },
            "expected": "success"  # Should handle gracefully
        },
        {
            "name": "Invalid metadata type (list)",
            "data": {
                "meeting_id": "test-456",
                "metadata": ["not", "a", "dict"],
                "recording_url": "http://example.com/audio.mp3"
            },
            "expected": "success"  # Should handle gracefully
        },
        {
            "name": "Invalid platform type (number)",
            "data": {
                "meeting_id": "test-789",
                "platform": 123,
                "recording_url": "http://example.com/audio.mp3"
            },
            "expected": "success"  # Should default to zoom
        },
        {
            "name": "Invalid start_time format",
            "data": {
                "meeting_id": "test-abc",
                "start_time": "not-a-date",
                "recording_url": "http://example.com/audio.mp3"
            },
            "expected": "success"  # Should use current time
        },
        {
            "name": "Valid complete data",
            "data": {
                "meeting_id": "valid-123",
                "topic": "Test Meeting",
                "platform": "zoom",
                "start_time": "2024-01-15T10:00:00",
                "participants": ["alice@test.com", "bob@test.com"],
                "recording_url": "http://example.com/audio.mp3",
                "metadata": {"key": "value"}
            },
            "expected": "success"
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        try:
            result = handler.handle_meeting_ended(test["data"])
            status = result.get("status")
            
            if status == test["expected"]:
                print(f"✅ PASS: {test['name']}")
                print(f"   Expected: {test['expected']}, Got: {status}")
                passed += 1
            else:
                print(f"❌ FAIL: {test['name']}")
                print(f"   Expected: {test['expected']}, Got: {status}")
                print(f"   Message: {result.get('message', 'No message')}")
                failed += 1
        except Exception as e:
            print(f"❌ ERROR: {test['name']}")
            print(f"   Exception: {str(e)}")
            failed += 1
        print()
    
    print(f"\nResults: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    return failed == 0


def test_meeting_processor_edge_cases():
    """Test meeting processor with invalid meeting objects."""
    print("\n" + "="*80)
    print("Testing Meeting Processor Edge Cases")
    print("="*80 + "\n")
    
    processor = MeetingProcessor()
    
    # Test 1: None meeting
    print("Test 1: None meeting object")
    result = processor.process_meeting_end(None)
    if result == (None, None):
        print("✅ PASS: Correctly handled None meeting\n")
    else:
        print("❌ FAIL: Did not handle None meeting correctly\n")
    
    # Test 2: Meeting without required fields
    print("Test 2: Meeting object missing status")
    class IncompleteMeeting:
        id = "test-123"
        # Missing status field
    
    result = processor.process_meeting_end(IncompleteMeeting())
    if result == (None, None):
        print("✅ PASS: Correctly handled incomplete meeting\n")
    else:
        print("❌ FAIL: Did not handle incomplete meeting correctly\n")
    
    # Test 3: Valid meeting should work
    print("Test 3: Valid meeting object")
    meeting = Meeting(
        id="valid-meeting",
        title="Test",
        platform=MeetingPlatform.ZOOM,
        start_time=datetime.utcnow(),
        status=MeetingStatus.ENDED,
        audio_url="http://example.com/audio.mp3"
    )
    transcription, summary = processor.process_meeting_end(meeting)
    if transcription and summary:
        print("✅ PASS: Successfully processed valid meeting\n")
    else:
        print("❌ FAIL: Failed to process valid meeting\n")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("EDGE CASE TESTING SUITE")
    print("="*80)
    
    success = True
    
    # Run all tests
    success = test_webhook_edge_cases() and success
    test_meeting_processor_edge_cases()
    
    print("\n" + "="*80)
    if success:
        print("✅ ALL TESTS PASSED")
    else:
        print("⚠️  SOME TESTS FAILED - See details above")
    print("="*80 + "\n")
