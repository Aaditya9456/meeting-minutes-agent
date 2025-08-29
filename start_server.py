#!/usr/bin/env python3
"""
Startup script for the Meeting Minutes Agent API
This script provides better error handling and startup messages
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check if required environment variables are set"""
    load_dotenv()
    
    required_vars = ["HF_TOKEN", "OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease create a .env file with the required variables.")
        print("You can copy env_template.txt to .env and fill in your values.")
        return False
    
    print("✅ Environment variables configured")
    return True

def main():
    """Main startup function"""
    print("🚀 Starting Meeting Minutes Agent API...")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("❌ main.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    print("✅ All checks passed")
    print("🌐 Starting server...")
    print("📖 API documentation will be available at: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/health")
    print("=" * 50)
    
    # Import and run the server
    try:
        from main import app
        import uvicorn
        from config import config
        
        uvicorn.run(
            "main:app",
            host=config.HOST,
            port=config.PORT,
            reload=config.DEBUG,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("   uv sync")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
