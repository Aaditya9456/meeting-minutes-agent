import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Meeting Minutes Agent API"""
    
    # API Configuration
    API_TITLE = "Meeting Minutes Agent API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "API for transcribing audio and generating meeting minutes"
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # API Keys
    HF_TOKEN = os.getenv("HF_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Transcription Configuration
    TRANSCRIPTION_MODEL = os.getenv("TRANSCRIPTION_MODEL", "openai/whisper-large-v3")
    TRANSCRIPTION_PROVIDER = os.getenv("TRANSCRIPTION_PROVIDER", "fal-ai")
    
    # File Upload Configuration
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 50 * 1024 * 1024))  # 50MB default
    ALLOWED_AUDIO_TYPES = [
        "audio/wav",
        "audio/mp3", 
        "audio/mpeg",
        "audio/flac",
        "audio/ogg",
        "audio/webm"
    ]
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        missing_vars = []
        
        if not cls.HF_TOKEN:
            missing_vars.append("HF_TOKEN")
        
        if not cls.OPENAI_API_KEY:
            missing_vars.append("OPENAI_API_KEY")
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True

# Create config instance
config = Config()
