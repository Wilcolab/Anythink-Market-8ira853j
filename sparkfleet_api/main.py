"""Main FastAPI application for SparkFleet Meeting Assistant."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .transcription.api import router as transcription_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="SparkFleet Smart Meeting Assistant API",
    description=(
        "API for automated meeting transcription, summarization, and action item tracking. "
        "Integrates with Zoom/GMeet to process meetings after they end."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transcription_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "SparkFleet Smart Meeting Assistant API",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Automated meeting transcription",
            "Meeting summarization",
            "Action item extraction",
            "Decision tracking",
            "Zoom/GMeet integration support"
        ],
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "sparkfleet-meeting-assistant"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
