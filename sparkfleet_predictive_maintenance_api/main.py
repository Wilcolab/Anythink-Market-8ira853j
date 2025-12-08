"""
Entry point for SparkFleet Smart Meeting Assistant API

Provides REST API endpoints for automated meeting transcription, 
summarization, and action item tracking.

See spec.md for requirements and acceptance criteria.
"""

import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import Dict

from .models import ProcessMeetingRequest, ProcessMeetingResponse, Transcript, Summary
from .transcription import MeetingProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# In-memory storage for demo purposes
# In production, this would use a proper database
meeting_storage: Dict[str, tuple[Transcript, Summary]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("Starting SparkFleet Smart Meeting Assistant API")
    yield
    logger.info("Shutting down SparkFleet Smart Meeting Assistant API")


# Initialize FastAPI application
app = FastAPI(
    title="SparkFleet Smart Meeting Assistant API",
    description="Automated transcription, summarization, and action item tracking for meetings",
    version="0.1.0",
    lifespan=lifespan
)

# Initialize meeting processor
meeting_processor = MeetingProcessor()


@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "name": "SparkFleet Smart Meeting Assistant API",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "process_meeting": "POST /meetings/process",
            "get_transcript": "GET /meetings/{meeting_id}/transcript",
            "get_summary": "GET /meetings/{meeting_id}/summary",
            "health": "GET /health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "meeting-assistant"}


@app.post("/meetings/process", response_model=ProcessMeetingResponse, status_code=status.HTTP_200_OK)
async def process_meeting(request: ProcessMeetingRequest):
    """
    Process a meeting recording to generate transcript and summary.
    
    This endpoint implements the core acceptance criterion:
    "Meetings can be transcribed and summarized automatically after call ends."
    
    Args:
        request: ProcessMeetingRequest containing audio path and metadata
        
    Returns:
        ProcessMeetingResponse with transcript and summary
        
    Raises:
        HTTPException: If processing fails
    """
    logger.info(f"Processing meeting request: {request.metadata.meeting_id}")
    
    try:
        # Process the meeting
        transcript, summary = meeting_processor.process_meeting(
            audio_file_path=request.audio_file_path,
            metadata=request.metadata,
            auto_summarize=request.auto_summarize
        )
        
        # Store results (in-memory for demo)
        meeting_storage[request.metadata.meeting_id] = (transcript, summary)
        
        # Build response
        response = ProcessMeetingResponse(
            meeting_id=request.metadata.meeting_id,
            status="completed",
            message="Meeting processed successfully",
            transcript=transcript,
            summary=summary
        )
        
        logger.info(f"Meeting {request.metadata.meeting_id} processed successfully")
        return response
        
    except ValueError as e:
        logger.error(f"Invalid request for meeting {request.metadata.meeting_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to process meeting {request.metadata.meeting_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process meeting: {str(e)}"
        )


@app.get("/meetings/{meeting_id}/transcript", response_model=Transcript)
async def get_transcript(meeting_id: str):
    """
    Retrieve the transcript for a processed meeting.
    
    Args:
        meeting_id: Unique meeting identifier
        
    Returns:
        Transcript object
        
    Raises:
        HTTPException: If meeting not found
    """
    logger.info(f"Retrieving transcript for meeting: {meeting_id}")
    
    if meeting_id not in meeting_storage:
        logger.warning(f"Meeting not found: {meeting_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meeting {meeting_id} not found"
        )
    
    transcript, _ = meeting_storage[meeting_id]
    return transcript


@app.get("/meetings/{meeting_id}/summary", response_model=Summary)
async def get_summary(meeting_id: str):
    """
    Retrieve the summary for a processed meeting.
    
    This endpoint provides access to:
    - Overall meeting summary
    - Key discussion points
    - Action items with confidence scores
    - Key decisions made
    
    Args:
        meeting_id: Unique meeting identifier
        
    Returns:
        Summary object with action items and decisions
        
    Raises:
        HTTPException: If meeting not found or summary not available
    """
    logger.info(f"Retrieving summary for meeting: {meeting_id}")
    
    if meeting_id not in meeting_storage:
        logger.warning(f"Meeting not found: {meeting_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meeting {meeting_id} not found"
        )
    
    _, summary = meeting_storage[meeting_id]
    
    if summary is None:
        logger.warning(f"Summary not available for meeting: {meeting_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Summary not available for meeting {meeting_id}"
        )
    
    return summary


@app.get("/meetings", response_model=Dict[str, str])
async def list_meetings():
    """
    List all processed meetings.
    
    Returns:
        Dictionary mapping meeting IDs to status
    """
    return {
        meeting_id: "completed"
        for meeting_id in meeting_storage.keys()
    }


if __name__ == "__main__":
    import uvicorn
    
    # Start the API server
    logger.info("Starting API server on http://0.0.0.0:8000")
    uvicorn.run(
        "sparkfleet_predictive_maintenance_api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
