import os
import tempfile
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn

from transcription import transcribe_audio
from agent import generate_meeting_minutes
from config import config

# Load environment variables
load_dotenv()

# Validate configuration
try:
    config.validate_config()
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please check your .env file and ensure all required variables are set.")
    exit(1)

app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION,
    debug=config.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscriptRequest(BaseModel):
    transcript: str

class MeetingMinutesResponse(BaseModel):
    transcript: str
    meeting_minutes: dict
    success: bool
    message: str

@app.get("/")
async def root():
    return {
        "message": "Meeting Minutes Agent API is running!",
        "version": config.API_VERSION,
        "endpoints": {
            "transcribe": "/transcribe - Upload audio and generate minutes",
            "transcribe_only": "/transcribe-only - Upload audio for transcription only",
            "generate_minutes": "/generate-minutes - Generate minutes from transcript text",
            "health": "/health - Health check"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "message": "API is operational",
        "config": {
            "transcription_model": config.TRANSCRIPTION_MODEL,
            "transcription_provider": config.TRANSCRIPTION_PROVIDER,
            "max_file_size": f"{config.MAX_FILE_SIZE / (1024*1024):.1f}MB"
        }
    }

@app.post("/transcribe", response_model=MeetingMinutesResponse)
async def transcribe_and_generate_minutes(
    file: UploadFile = File(...),
    generate_minutes: bool = Form(True)
):
    """
    Transcribe audio file and optionally generate meeting minutes
    """
    try:
        # Validate file type
        if file.content_type not in config.ALLOWED_AUDIO_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file.content_type} not supported. Allowed types: {config.ALLOWED_AUDIO_TYPES}"
            )
        
        # Check file size
        if file.size and file.size > config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {config.MAX_FILE_SIZE / (1024*1024):.1f}MB"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Transcribe audio
            transcript = transcribe_audio(temp_file_path)
            
            print(f"Transcription result type: {type(transcript)}")
            print(f"Transcription result: {transcript}")

            if not transcript:
                raise HTTPException(status_code=500, detail="Transcription failed")
            
            # Generate meeting minutes if requested
            meeting_minutes = None
            if generate_minutes:
                try:
                    meeting_minutes = await generate_meeting_minutes(transcript)
                    print(f"Generated meeting minutes: {meeting_minutes}")
                except Exception as e:
                    print(f"Error generating meeting minutes: {e}")
                    # Continue with just transcription if meeting minutes generation fails
                    meeting_minutes = {
                        "summary": "Error generating meeting minutes",
                        "decisions": [],
                        "action_items": [],
                        "error": str(e)
                    }
            return MeetingMinutesResponse(
                transcript=transcript,
                meeting_minutes=meeting_minutes or {},
                success=True,
                message="Audio transcribed successfully"
            )
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

@app.post("/generate-minutes", response_model=MeetingMinutesResponse)
async def generate_minutes_from_transcript(request: TranscriptRequest):
    """
    Generate meeting minutes from existing transcript text
    """
    try:
        if not request.transcript.strip():
            raise HTTPException(status_code=400, detail="Transcript cannot be empty")
        
        meeting_minutes = await generate_meeting_minutes(request.transcript)
        
        return MeetingMinutesResponse(
            transcript=request.transcript,
            meeting_minutes=meeting_minutes,
            success=True,
            message="Meeting minutes generated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating meeting minutes: {str(e)}")

@app.post("/transcribe-only")
async def transcribe_only(file: UploadFile = File(...)):
    """
    Only transcribe audio without generating meeting minutes
    """
    try:
        # Validate file type
        if file.content_type not in config.ALLOWED_AUDIO_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file.content_type} not supported. Allowed types: {config.ALLOWED_AUDIO_TYPES}"
            )
        
        # Check file size
        if file.size and file.size > config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {config.MAX_FILE_SIZE / (1024*1024):.1f}MB"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Transcribe audio
            transcript = transcribe_audio(temp_file_path)
            
            print(f"Transcription result type: {type(transcript)}")
            print(f"Transcription result: {transcript}")
            
            if not transcript:
                raise HTTPException(status_code=500, detail="Transcription failed")
            
            return {
                "transcript": transcript,
                "success": True,
                "message": "Audio transcribed successfully"
            }
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

if __name__ == "__main__":
    print(f"Starting Meeting Minutes Agent API on {config.HOST}:{config.PORT}")
    print(f"Debug mode: {config.DEBUG}")
    
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
