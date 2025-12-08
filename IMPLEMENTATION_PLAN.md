# Implementation Plan: Automated Meeting Transcription & Summarization

**Feature**: Meetings can be transcribed and summarized automatically after call ends

**Spec Reference**: spec.md - Functional Requirement #1 & Acceptance Criteria  
**Issue**: Automated Transcription & Summarization  
**Target Modules**: `sparkfleet_predictive_maintenance_api/transcription/`, `task_tracking/`, `user_workflow/`

---

## Overview

This plan outlines the step-by-step implementation for automatically transcribing and summarizing meetings after they end. The feature addresses the core acceptance criterion from spec.md:

> "Meetings can be transcribed and summarized automatically after call ends."

The implementation will integrate with Zoom/GMeet, process audio recordings, generate summaries, extract action items, and make results available in the SparkFleet UI within 5 minutes.

---

## Dependencies & Prerequisites

### External Services
- **Transcription API**: Whisper (OpenAI), Google Speech-to-Text, or Azure Speech Services
- **AI/LLM API**: OpenAI GPT-4 or Anthropic Claude for summarization
- **Meeting Platforms**: Zoom API and/or Google Meet API for webhooks and audio access

### Infrastructure
- **Database**: PostgreSQL for storing meetings, transcripts, summaries, and action items
- **Message Queue**: Redis + Celery (or similar) for async job processing
- **Storage**: S3-compatible storage for audio files and transcripts
- **API Framework**: FastAPI (already in requirements.txt)

### Python Dependencies (to add to requirements.txt)
```python
# AI/Transcription
openai>=1.3.0
anthropic>=0.7.0
# whisper>=1.0.0  # If using local Whisper

# Task Queue
celery>=5.3.0
redis>=5.0.0

# Audio Processing
pydub>=0.25.1
```

---

## Phase 1: Core Infrastructure Setup

**Goal**: Set up FastAPI application and database models

### Step 1.1: FastAPI Application Structure
**File**: `sparkfleet_predictive_maintenance_api/main.py`

- [ ] Initialize FastAPI app with CORS middleware
- [ ] Configure environment variables using python-dotenv
- [ ] Set up application logging (structured logging)
- [ ] Create health check endpoint (`GET /health`)
- [ ] Add startup/shutdown event handlers

**References**:
- spec.md: Non-Functional Requirements - Usability
- requirements.txt: FastAPI already included

### Step 1.2: Database Models
**New File**: `sparkfleet_predictive_maintenance_api/models.py`

- [ ] Create `Meeting` model (id, title, start_time, end_time, participants, platform, audio_url, status)
- [ ] Create `Transcript` model (id, meeting_id, text, confidence_score, created_at)
- [ ] Create `Summary` model (id, meeting_id, content, key_points, decisions, created_at)
- [ ] Create `ActionItem` model (id, meeting_id, text, assignee, confidence_score, deadline)
- [ ] Set up SQLAlchemy engine and session management

**References**:
- spec.md: Functional Requirement #1 - Extract action items
- requirements.txt: SQLAlchemy already included

### Step 1.3: Database Migrations
**New File**: `sparkfleet_predictive_maintenance_api/alembic/`

- [ ] Initialize Alembic for database migrations
- [ ] Create initial migration for all models
- [ ] Add migration script to create tables

**References**:
- requirements.txt: Alembic already included

---

## Phase 2: Meeting Webhook & Audio Handler

**Goal**: Receive meeting end notifications and download audio files

### Step 2.1: Webhook Endpoint for Meeting End
**File**: `sparkfleet_predictive_maintenance_api/main.py`

- [ ] Create `POST /api/webhooks/meeting-ended` endpoint
- [ ] Validate webhook signature (Zoom/GMeet authentication)
- [ ] Extract meeting metadata (id, participants, duration, audio_url)
- [ ] Create Meeting record in database with status='pending'
- [ ] Queue transcription job asynchronously
- [ ] Return 200 OK response immediately

**References**:
- spec.md: Functional Requirement #1 - Transcribe meeting audio from Zoom/GMeet
- spec.md: Dependencies - "Assumes Zoom/GMeet integrations already available"

### Step 2.2: Audio Download Handler
**New File**: `sparkfleet_predictive_maintenance_api/audio_handler.py`

- [ ] Implement `download_audio(meeting_id, audio_url)` function
- [ ] Download audio file from Zoom/GMeet URL with retry logic
- [ ] Validate audio file (format: mp3/wav/m4a, size limits, duration)
- [ ] Upload to S3-compatible storage
- [ ] Store storage URL in Meeting record
- [ ] Handle download failures with appropriate error logging

**References**:
- spec.md: Non-Functional Requirements - Reliability
- transcription/TODO.md: "Implement audio input handler for Zoom/GMeet recordings"

---

## Phase 3: Transcription Implementation

**Goal**: Convert audio to text using transcription API

### Step 3.1: Transcriber Class Implementation
**File**: `sparkfleet_predictive_maintenance_api/transcription/transcriber.py`

- [ ] Implement `Transcriber.__init__(api_key)` with API client initialization
- [ ] Implement `transcribe_audio(audio_file_path)` method:
  - [ ] Load audio file from storage
  - [ ] Call Whisper API (or alternative) with audio data
  - [ ] Handle API rate limits and retries
  - [ ] Parse response to extract text and confidence scores
  - [ ] Return dict with 'text', 'confidence', 'duration'
- [ ] Implement `transcribe_stream()` for large files (chunking)
- [ ] Add error handling for API failures, invalid audio, timeouts

**References**:
- spec.md: Functional Requirement #1 - "Transcribe meeting audio"
- transcription/TODO.md: "Integrate transcription API (Whisper or similar)"
- transcription/transcriber.py: Existing stub with TODOs

### Step 3.2: Transcription Service
**New File**: `sparkfleet_predictive_maintenance_api/transcription/service.py`

- [ ] Create `TranscriptionService` class
- [ ] Implement `process_meeting_transcription(meeting_id)`:
  - [ ] Retrieve Meeting record from database
  - [ ] Download audio using audio_handler
  - [ ] Call Transcriber.transcribe_audio()
  - [ ] Create Transcript record with results
  - [ ] Update Meeting status to 'transcribed'
  - [ ] Queue summarization job
  - [ ] Log processing time (target: <5 minutes total)

**References**:
- spec.md: Non-Functional Requirements - Performance (5-minute target)

---

## Phase 4: Summarization & Extraction

**Goal**: Generate summaries and extract action items from transcripts

### Step 4.1: Summarizer Class Implementation
**File**: `sparkfleet_predictive_maintenance_api/transcription/summarizer.py`

- [ ] Implement `Summarizer.__init__()` with LLM API client
- [ ] Implement `summarize(transcript)` method:
  - [ ] Create prompt for LLM: "Summarize this meeting transcript..."
  - [ ] Call OpenAI GPT-4 or Claude API
  - [ ] Parse response to extract summary, key_points, decisions
  - [ ] Return dict with structured data
- [ ] Add error handling and retry logic

**References**:
- spec.md: Functional Requirement #1 - "Summarize key discussion points and decisions"
- transcription/TODO.md: "Build summarization engine for key discussion points"
- transcription/summarizer.py: Existing stub with TODOs

### Step 4.2: Action Item Extraction
**File**: `sparkfleet_predictive_maintenance_api/transcription/summarizer.py`

- [ ] Implement `extract_action_items(transcript)` method:
  - [ ] Create prompt: "Extract action items, especially 'You said you would...' statements"
  - [ ] Call LLM API with specialized prompt
  - [ ] Parse response to extract: text, assignee, deadline
  - [ ] Calculate confidence score (0.0-1.0) based on clarity
  - [ ] Return list of action item dicts
- [ ] Implement pattern matching for "You said you would..." phrases
- [ ] Handle ambiguous items (low confidence < 0.7)

**References**:
- spec.md: Functional Requirement #1 - "Extract action items (e.g., 'You said you would...')"
- spec.md: Functional Requirement #2 - "Show confidence scores for extracted items"
- transcription/TODO.md: "Extract action items with 'You said you would...' detection"

### Step 4.3: Decision Extraction
**File**: `sparkfleet_predictive_maintenance_api/transcription/summarizer.py`

- [ ] Implement `extract_decisions(transcript)` method:
  - [ ] Create prompt: "Extract key decisions made in this meeting"
  - [ ] Call LLM API
  - [ ] Parse decisions with context
  - [ ] Calculate confidence scores
  - [ ] Return list of decision dicts

**References**:
- spec.md: Functional Requirement #1 - "Summarize key discussion points and decisions"
- spec.md: Acceptance Criteria - "Key decisions captured and displayed"

### Step 4.4: Summarization Service
**New File**: `sparkfleet_predictive_maintenance_api/transcription/summary_service.py`

- [ ] Create `SummaryService` class
- [ ] Implement `process_meeting_summary(meeting_id)`:
  - [ ] Retrieve Transcript from database
  - [ ] Call Summarizer.summarize()
  - [ ] Call Summarizer.extract_action_items()
  - [ ] Call Summarizer.extract_decisions()
  - [ ] Store Summary record in database
  - [ ] Store ActionItem records in database
  - [ ] Update Meeting status to 'completed'
  - [ ] Trigger notification to SparkFleet UI
  - [ ] Log total processing time

**References**:
- spec.md: Functional Requirement #1 - "Display summary and action items inside SparkFleet UI"

---

## Phase 5: Async Processing Pipeline

**Goal**: Orchestrate transcription → summarization workflow asynchronously

### Step 5.1: Celery Task Queue Setup
**New File**: `sparkfleet_predictive_maintenance_api/tasks.py`

- [ ] Configure Celery with Redis broker
- [ ] Create `@celery.task` for `transcribe_meeting_task(meeting_id)`
- [ ] Create `@celery.task` for `summarize_meeting_task(meeting_id)`
- [ ] Implement task chaining: transcribe → summarize
- [ ] Add error handling and retry logic (max 3 retries)
- [ ] Set task timeouts (10 minutes per task)

**References**:
- spec.md: Non-Functional Requirements - Performance (5-minute target)
- spec.md: Non-Functional Requirements - Scalability

### Step 5.2: Job Status Tracking
**File**: `sparkfleet_predictive_maintenance_api/models.py`

- [ ] Add status tracking fields to Meeting model: 
  - status: 'pending', 'downloading', 'transcribing', 'summarizing', 'completed', 'failed'
  - error_message: text field for failures
  - processing_started_at, processing_completed_at
- [ ] Create database migration for new fields

### Step 5.3: Progress Monitoring
**New File**: `sparkfleet_predictive_maintenance_api/monitoring.py`

- [ ] Implement `get_meeting_status(meeting_id)` function
- [ ] Implement `get_processing_metrics()` (avg time, success rate)
- [ ] Add logging for each pipeline stage
- [ ] Track processing time to ensure <5 minute SLA

**References**:
- spec.md: Non-Functional Requirements - Performance
- spec.md: User Workflow - "Dashboard showing meetings needing follow-up"

---

## Phase 6: API Endpoints & UI Integration

**Goal**: Expose meeting summaries via REST API

### Step 6.1: Meeting Summary Endpoints
**File**: `sparkfleet_predictive_maintenance_api/main.py`

- [ ] `GET /api/meetings/{meeting_id}/summary` - Get full summary for a meeting
  - [ ] Return: summary, key_points, decisions, action_items, confidence_scores
  - [ ] Include transcript if requested (?include_transcript=true)
  - [ ] Check user permissions (only authorized users)
- [ ] `GET /api/meetings` - List all meetings with status
  - [ ] Support filtering by date, status, participant
  - [ ] Pagination support (page, per_page params)
  - [ ] Return basic meeting info + processing status
- [ ] `POST /api/meetings/{meeting_id}/transcribe` - Manually trigger transcription
  - [ ] Useful for reprocessing or testing
  - [ ] Queue transcription job
  - [ ] Return job_id for tracking

**References**:
- spec.md: Functional Requirement #1 - "Display summary and action items inside SparkFleet UI"
- spec.md: Functional Requirement #4 - Dashboard showing meetings

### Step 6.2: Action Items Endpoints
**File**: `sparkfleet_predictive_maintenance_api/main.py`

- [ ] `GET /api/action-items` - List all action items
  - [ ] Filter by: meeting_id, assignee, status, confidence
  - [ ] Support sorting by deadline, confidence
  - [ ] Pagination
- [ ] `PATCH /api/action-items/{item_id}` - Update action item
  - [ ] Allow user to edit text, assignee, deadline
  - [ ] Mark as confirmed/revised by user

**References**:
- spec.md: Functional Requirement #4 - "Allow users to approve or revise AI-generated summaries"
- task_tracking/TODO.md: Task CRUD operations

### Step 6.3: Webhook Callback to SparkFleet UI
**File**: `sparkfleet_predictive_maintenance_api/transcription/summary_service.py`

- [ ] When meeting processing completes, send webhook to SparkFleet UI
- [ ] Include: meeting_id, status, summary_url
- [ ] Trigger UI notification/update

**References**:
- spec.md: Functional Requirement #1 - "Display summary inside SparkFleet UI after meeting"

---

## Phase 7: Security & Compliance

**Goal**: Implement security, permissions, and consent management

### Step 7.1: User Consent Verification
**New File**: `sparkfleet_predictive_maintenance_api/non_functional/consent.py`

- [ ] Create `check_consent(meeting_id, user_id)` function
- [ ] Store user consent in database (consent_given, timestamp)
- [ ] Block transcription if consent not obtained
- [ ] Add UI prompt for consent before recording

**References**:
- spec.md: Non-Functional Requirements - Compliance
- spec.md: Acceptance Criteria - "Consent requirements enforced"
- non_functional/compliance.py: Stub for compliance features

### Step 7.2: Permission & Access Control
**File**: `sparkfleet_predictive_maintenance_api/non_functional/security.py`

- [ ] Implement `check_meeting_access(user_id, meeting_id)` function
- [ ] Only meeting participants can view summaries
- [ ] Add role-based access (admin can view all)
- [ ] Apply permission checks to all API endpoints

**References**:
- spec.md: Non-Functional Requirements - Security
- spec.md: Acceptance Criteria - "Only authorized users can view summaries"
- non_functional/security.py: Stub for security features

### Step 7.3: PII Detection & Redaction (Optional)
**New File**: `sparkfleet_predictive_maintenance_api/non_functional/pii_handler.py`

- [ ] Implement PII detection in transcripts (SSN, credit cards, etc.)
- [ ] Redact or flag sensitive information
- [ ] Log PII detections for audit

**References**:
- spec.md: Non-Functional Requirements - Security (PII protection)

### Step 7.4: Audit Logging
**File**: `sparkfleet_predictive_maintenance_api/non_functional/security.py`

- [ ] Log all access to transcripts and summaries
- [ ] Log who viewed what and when
- [ ] Store audit logs separately from application logs

**References**:
- spec.md: Non-Functional Requirements - Security (audit logging)

---

## Phase 8: Testing & Validation

**Goal**: Ensure reliability and accuracy

### Step 8.1: Unit Tests
**New Directory**: `tests/`

- [ ] Test `Transcriber.transcribe_audio()` with sample audio files
- [ ] Test `Summarizer.summarize()` with sample transcripts
- [ ] Test `Summarizer.extract_action_items()` pattern matching
- [ ] Test permission checks and access control
- [ ] Mock external API calls (Whisper, OpenAI)

**Test Files to Create**:
- `tests/test_transcriber.py`
- `tests/test_summarizer.py`
- `tests/test_security.py`
- `tests/test_api_endpoints.py`

**References**:
- requirements.txt: pytest already included
- spec.md: Non-Functional Requirements - Reliability (90%+ accuracy)

### Step 8.2: Integration Tests
**New File**: `tests/test_integration.py`

- [ ] Test full pipeline: webhook → transcribe → summarize → notify
- [ ] Test with real audio files (various lengths: 5min, 30min, 1hr)
- [ ] Test with different audio formats (mp3, wav, m4a)
- [ ] Validate 5-minute processing time target
- [ ] Test failure scenarios: bad audio, API timeout, etc.

### Step 8.3: Accuracy Validation
**New File**: `tests/test_accuracy.py`

- [ ] Create test dataset with known action items
- [ ] Measure action item detection rate (target: >90%)
- [ ] Test "You said you would..." pattern detection
- [ ] Validate confidence score calibration
- [ ] Test with various meeting types (sales, PM, customer success)

**References**:
- spec.md: Non-Functional Requirements - Reliability (90%+ actionable detection rate)

### Step 8.4: Performance Testing
**New File**: `tests/test_performance.py`

- [ ] Measure transcription time for various audio lengths
- [ ] Measure summarization time
- [ ] Validate total processing time < 5 minutes
- [ ] Test concurrent processing (scalability)

**References**:
- spec.md: Non-Functional Requirements - Performance (5-minute target)
- spec.md: Non-Functional Requirements - Scalability

---

## Phase 9: Documentation & Deployment

**Goal**: Production-ready deployment and user documentation

### Step 9.1: API Documentation
**File**: `sparkfleet_predictive_maintenance_api/main.py`

- [ ] Add OpenAPI/Swagger documentation to all endpoints
- [ ] Include request/response examples
- [ ] Document authentication requirements
- [ ] Generate interactive API docs at `/docs`

### Step 9.2: Setup & Configuration Guide
**New File**: `docs/SETUP.md`

- [ ] Document environment variables needed
- [ ] Document external API key setup (Whisper, OpenAI)
- [ ] Document Zoom/GMeet webhook configuration
- [ ] Document database setup and migrations
- [ ] Document Redis/Celery setup

### Step 9.3: Zoom/GMeet Integration Guide
**New File**: `docs/INTEGRATION.md`

- [ ] Step-by-step Zoom webhook setup
- [ ] Step-by-step Google Meet API setup
- [ ] Webhook URL configuration
- [ ] Authentication setup
- [ ] Testing webhook delivery

**References**:
- spec.md: Dependencies - "Zoom/GMeet integrations already available"

### Step 9.4: Deployment Guide
**New File**: `docs/DEPLOYMENT.md`

- [ ] Infrastructure requirements (servers, storage, database)
- [ ] Docker/container setup instructions
- [ ] Environment configuration for production
- [ ] Monitoring and alerting setup
- [ ] Backup and disaster recovery procedures

### Step 9.5: Operational Runbook
**New File**: `docs/RUNBOOK.md`

- [ ] Common issues and troubleshooting
- [ ] How to monitor processing queue
- [ ] How to reprocess failed meetings
- [ ] Performance tuning guidelines
- [ ] Scaling guidelines

**References**:
- spec.md: Non-Functional Requirements - Scalability

---

## Implementation Timeline & Dependencies

### Phase Order & Dependencies

```
Phase 1 (Infrastructure) → Phase 2 (Webhooks) → Phase 3 (Transcription)
                                                          ↓
Phase 5 (Async Pipeline) ←───────────────────── Phase 4 (Summarization)
         ↓
Phase 6 (API Endpoints) ← Phase 7 (Security)
         ↓
Phase 8 (Testing) → Phase 9 (Documentation)
```

### Estimated Effort
- **Phase 1-2**: 3-5 days (infrastructure + webhooks)
- **Phase 3**: 3-4 days (transcription integration)
- **Phase 4**: 4-5 days (summarization + extraction)
- **Phase 5**: 2-3 days (async processing)
- **Phase 6**: 2-3 days (API endpoints)
- **Phase 7**: 3-4 days (security + compliance)
- **Phase 8**: 5-7 days (comprehensive testing)
- **Phase 9**: 2-3 days (documentation)

**Total Estimated Time**: 24-34 days

---

## Success Criteria Checklist

Per spec.md Acceptance Criteria:

- [ ] Meetings can be transcribed and summarized automatically after call ends
- [ ] Key decisions and "You said you would..." actions are captured and displayed in SparkFleet
- [ ] Action items can be sent to GitHub Issues, calendar, and Slack/email (integration phase - separate from this plan)
- [ ] Users can approve or edit AI summary and action items before distribution
- [ ] Dashboard displays meetings needing follow-up, including status and deadlines
- [ ] Confidence scores and "Need clarification" tags shown for uncertain extracted items
- [ ] Only authorized users can view summaries and decision history
- [ ] Summaries available within 5 minutes after meeting ends
- [ ] No external tool installation required; all functionality operates inside SparkFleet
- [ ] Consent requirements are enforced before any recording or transcription

---

## Next Steps

1. **Immediate**: Set up development environment with required API keys
2. **Week 1**: Complete Phase 1-2 (infrastructure + webhooks)
3. **Week 2**: Complete Phase 3 (transcription)
4. **Week 3**: Complete Phase 4-5 (summarization + async processing)
5. **Week 4**: Complete Phase 6-7 (API + security)
6. **Week 5+**: Testing, documentation, and production deployment

---

## References

- **spec.md**: Complete functional and non-functional requirements
- **sparkfleet_predictive_maintenance_api/transcription/TODO.md**: Transcription-specific tasks
- **sparkfleet_predictive_maintenance_api/TODO.md**: Master TODO list
- **requirements.txt**: Current dependencies
