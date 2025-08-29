#!/usr/bin/env python3
"""
Demo Startup Script for Meeting Minutes Agent
This script starts the FastAPI backend and provides instructions for the frontend
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_banner():
    """Print a nice banner"""
    print("=" * 60)
    print("🚀 MEETING MINUTES AGENT - DEMO MODE")
    print("=" * 60)
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import huggingface_hub
        import openai
        print("✅ All Python dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: uv sync")
        return False

def check_environment():
    """Check environment variables"""
    print("🔍 Checking environment variables...")
    
    load_dotenv()
    required_vars = ["HF_TOKEN", "OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please create a .env file with your API keys")
        print("You can copy env_template.txt to .env and fill in your values")
        return False
    
    print("✅ Environment variables configured")
    return True

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    
    try:
        # Start the backend server
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for server to start
        time.sleep(3)
        
        # Check if server is running
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend server is running on http://localhost:8000")
                return process
            else:
                print("❌ Backend server failed to start properly")
                return None
        except:
            print("❌ Backend server failed to start properly")
            return None
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_frontend():
    """Start the Next.js frontend"""
    print("🌐 Starting Next.js frontend...")
    
    frontend_dir = Path("meeing_minutes_agent")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return None
    
    try:
        # Check if node_modules exists
        if not (frontend_dir / "node_modules").exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        
        # Start the frontend
        process = subprocess.Popen([
            "npm", "run", "dev"
        ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for frontend to start
        time.sleep(5)
        
        print("✅ Frontend is starting on http://localhost:3000")
        return process
        
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def main():
    """Main function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    print("🎯 Starting Meeting Minutes Agent Demo...")
    print()
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend. Exiting.")
        sys.exit(1)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend. Backend is still running.")
        print("You can access the API at: http://localhost:8000")
        print("API docs: http://localhost:8000/docs")
    
    print()
    print("=" * 60)
    print("🎉 DEMO IS READY!")
    print("=" * 60)
    print()
    print("📱 Frontend: http://localhost:3000")
    print("🔧 Backend API: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print()
    print("💡 How to use:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Upload an audio file (MP3, WAV, FLAC, etc.)")
    print("3. Wait for transcription and meeting minutes generation")
    print("4. View the structured results in the UI")
    print()
    print("⚠️  Press Ctrl+C to stop both servers")
    print()
    
    try:
        # Open frontend in browser
        if frontend_process:
            time.sleep(2)
            webbrowser.open("http://localhost:3000")
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        
        if backend_process:
            backend_process.terminate()
            print("✅ Backend server stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend server stopped")
        
        print("👋 Demo stopped. Goodbye!")

if __name__ == "__main__":
    try:
        from dotenv import load_dotenv
        main()
    except ImportError:
        print("❌ python-dotenv not found. Please install it:")
        print("   uv add python-dotenv")
        sys.exit(1)
