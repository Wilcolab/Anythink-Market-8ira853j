# SparkFleet Smart Meeting Assistant - API Usage Guide

This guide explains how to use the REST API for automated meeting transcription and summarization.

## Quick Start

### Starting the API Server

```bash
# From the project root directory
python -m sparkfleet_predictive_maintenance_api.main
```

The API will be available at `http://localhost:8000`

### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### 1. Process a Meeting

**Endpoint:** `POST /meetings/process`

Transcribes and summarizes a meeting recording. This is the main endpoint for the automatic meeting processing workflow.

**Request Body:**
```json
{
  "audio_file_path": "/path/to/meeting-recording.mp3",
  "metadata": {
    "meeting_id": "meeting_20251208_001",
    "title": "Q4 Planning Meeting",
    "participants": ["Alice", "Bob", "Charlie"],
    "start_time": "2025-12-08T10:00:00",
    "end_time": "2025-12-08T11:00:00",
    "platform": "zoom"
  },
  "auto_summarize": true
}
```

**Response (200 OK):**
```json
{
  "meeting_id": "meeting_20251208_001",
  "status": "completed",
  "message": "Meeting processed successfully",
  "transcript": {
    "meeting_id": "meeting_20251208_001",
    "text": "Full meeting transcript...",
    "confidence": 0.92,
    "language": "en",
    "duration_seconds": 3600,
    "created_at": "2025-12-08T11:01:00"
  },
  "summary": {
    "meeting_id": "meeting_20251208_001",
    "summary_text": "Meeting summary...",
    "key_points": [
      "Discussed Q4 roadmap",
      "Reviewed budget allocation"
    ],
    "action_items": [
      {
        "text": "complete the API documentation by Friday",
        "assignee": "Alice",
        "confidence": 0.95,
        "deadline": null,
        "needs_clarification": false
      }
    ],
    "decisions": [
      {
        "decision": "to launch MVP by end of Q4",
        "context": "Team agreed to prioritize...",
        "confidence": 0.90,
        "timestamp": "00:15"
      }
    ],
    "generated_at": "2025-12-08T11:01:05"
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/meetings/process \
  -H "Content-Type: application/json" \
  -d '{
    "audio_file_path": "/tmp/meeting.mp3",
    "metadata": {
      "meeting_id": "test_001",
      "title": "Team Standup",
      "participants": ["Alice", "Bob"],
      "start_time": "2025-12-08T10:00:00",
      "platform": "zoom"
    },
    "auto_summarize": true
  }'
```

### 2. Get Meeting Transcript

**Endpoint:** `GET /meetings/{meeting_id}/transcript`

Retrieves the transcript for a previously processed meeting.

**Response (200 OK):**
```json
{
  "meeting_id": "meeting_20251208_001",
  "text": "Full transcript text...",
  "confidence": 0.92,
  "language": "en",
  "duration_seconds": 3600,
  "created_at": "2025-12-08T11:01:00"
}
```

**cURL Example:**
```bash
curl http://localhost:8000/meetings/test_001/transcript
```

### 3. Get Meeting Summary

**Endpoint:** `GET /meetings/{meeting_id}/summary`

Retrieves the summary, action items, and decisions for a processed meeting.

**Response (200 OK):**
```json
{
  "meeting_id": "meeting_20251208_001",
  "summary_text": "Overall meeting summary...",
  "key_points": ["Point 1", "Point 2"],
  "action_items": [...],
  "decisions": [...],
  "generated_at": "2025-12-08T11:01:05"
}
```

**cURL Example:**
```bash
curl http://localhost:8000/meetings/test_001/summary
```

### 4. List All Meetings

**Endpoint:** `GET /meetings`

Returns a list of all processed meetings.

**Response (200 OK):**
```json
{
  "meeting_001": "completed",
  "meeting_002": "completed"
}
```

**cURL Example:**
```bash
curl http://localhost:8000/meetings
```

### 5. Health Check

**Endpoint:** `GET /health`

Check if the API is running and healthy.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "meeting-assistant"
}
```

**cURL Example:**
```bash
curl http://localhost:8000/health
```

## Response Codes

- `200 OK` - Request successful
- `400 Bad Request` - Invalid request (e.g., file not found, unsupported format)
- `404 Not Found` - Meeting not found
- `500 Internal Server Error` - Server error during processing

## Data Models

### ActionItem
```json
{
  "text": "Action item description",
  "assignee": "Person responsible (or null)",
  "confidence": 0.95,
  "deadline": "2025-12-15T00:00:00",
  "needs_clarification": false
}
```

**Confidence Levels:**
- 0.90-1.0: Explicit commitment ("You said you would...")
- 0.80-0.89: Clear statement ("I'll...")
- 0.70-0.79: Implied action ("should", "need to")

### Decision
```json
{
  "decision": "Description of the decision",
  "context": "Surrounding context",
  "confidence": 0.90,
  "timestamp": "00:15"
}
```

## Python Client Example

```python
import requests
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

# Process a meeting
response = requests.post(
    f"{BASE_URL}/meetings/process",
    json={
        "audio_file_path": "/path/to/recording.mp3",
        "metadata": {
            "meeting_id": "meeting_001",
            "title": "Team Sync",
            "participants": ["Alice", "Bob"],
            "start_time": datetime.utcnow().isoformat(),
            "platform": "zoom"
        },
        "auto_summarize": True
    }
)

if response.status_code == 200:
    result = response.json()
    print(f"Meeting processed: {result['meeting_id']}")
    print(f"Action items: {len(result['summary']['action_items'])}")
    
    # Get action items
    for item in result['summary']['action_items']:
        print(f"- {item['text']} ({item['assignee']})")
else:
    print(f"Error: {response.status_code}")
    print(response.json())

# Retrieve summary later
summary_response = requests.get(f"{BASE_URL}/meetings/meeting_001/summary")
if summary_response.status_code == 200:
    summary = summary_response.json()
    print(f"Summary: {summary['summary_text']}")
```

## JavaScript/TypeScript Client Example

```typescript
const BASE_URL = "http://localhost:8000";

// Process a meeting
async function processMeeting() {
  const response = await fetch(`${BASE_URL}/meetings/process`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      audio_file_path: "/path/to/recording.mp3",
      metadata: {
        meeting_id: "meeting_001",
        title: "Team Sync",
        participants: ["Alice", "Bob"],
        start_time: new Date().toISOString(),
        platform: "zoom",
      },
      auto_summarize: true,
    }),
  });

  if (response.ok) {
    const result = await response.json();
    console.log(`Meeting processed: ${result.meeting_id}`);
    console.log(`Action items: ${result.summary.action_items.length}`);
    return result;
  } else {
    throw new Error(`Failed to process meeting: ${response.status}`);
  }
}

// Get summary
async function getSummary(meetingId: string) {
  const response = await fetch(`${BASE_URL}/meetings/${meetingId}/summary`);
  if (response.ok) {
    return await response.json();
  }
  throw new Error(`Failed to get summary: ${response.status}`);
}
```

## Integration Patterns

### Automatic Processing on Meeting End

To automatically process meetings when they end, you can:

1. **Webhook Integration**: Configure Zoom/GMeet to send webhooks when recordings are ready
2. **Polling**: Periodically check for new recordings
3. **Event-Driven**: Use calendar events to trigger processing

Example webhook handler:
```python
from fastapi import Request

@app.post("/webhooks/zoom/recording-ready")
async def handle_zoom_recording(request: Request):
    data = await request.json()
    
    # Extract meeting details from webhook
    meeting_id = data['object']['id']
    download_url = data['download_url']
    
    # Download recording
    audio_path = download_recording(download_url)
    
    # Process meeting
    response = requests.post(
        f"{BASE_URL}/meetings/process",
        json={
            "audio_file_path": audio_path,
            "metadata": {
                "meeting_id": meeting_id,
                "title": data['object']['topic'],
                "participants": data['object']['participants'],
                "start_time": data['object']['start_time'],
                "platform": "zoom"
            },
            "auto_summarize": True
        }
    )
    
    return {"status": "processing"}
```

## Best Practices

1. **Use unique meeting IDs**: Ensure meeting_id is unique to avoid conflicts
2. **Handle timeouts**: Large meetings may take longer to process
3. **Implement retry logic**: For production use, add exponential backoff for failed requests
4. **Store results**: Save transcripts and summaries to a database for persistence
5. **Monitor confidence scores**: Review items with low confidence scores manually
6. **Validate audio files**: Check file exists and format is supported before processing

## Troubleshooting

### Common Errors

**400 Bad Request: "Audio file not found"**
- Ensure the file path is absolute and the file exists
- Check file permissions

**400 Bad Request: "Unsupported audio format"**
- Supported formats: .mp3, .wav, .m4a, .ogg, .flac
- Convert file to a supported format

**404 Not Found: "Meeting not found"**
- Meeting hasn't been processed yet
- Check the meeting_id is correct
- In current implementation, data is stored in-memory and lost on restart

**500 Internal Server Error**
- Check server logs for details
- Ensure all dependencies are installed
- Verify sufficient disk space and memory

## Support

For issues or questions:
- Check the test suite in `tests/` for examples
- Review `example_usage.py` for a complete working example
- See the main `README.md` for project overview
