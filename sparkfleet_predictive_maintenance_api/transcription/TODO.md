# Transcription & Summarization - TODO

## Spec Reference
Functional Requirement #1: Automated Transcription & Summarization

## Tasks
- [ ] Implement audio input handler for Zoom/GMeet recordings
- [ ] Integrate transcription API (Whisper or similar)
- [ ] Build summarization engine for key discussion points
- [ ] Extract action items with "You said you would..." detection
- [ ] Display summary and action items in SparkFleet UI
- [ ] Add confidence scoring for extracted items
- [ ] Implement post-processing pipeline (5-minute target)

## Acceptance Criteria
- [ ] Meetings can be transcribed automatically after call ends
- [ ] Key decisions and action items are captured and displayed
- [ ] Summaries available within 5 minutes after meeting ends

## Dependencies
- External transcription API (Whisper or in-house model)
- Zoom/GMeet integration for audio access
