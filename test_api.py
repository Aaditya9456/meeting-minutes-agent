#!/usr/bin/env python3
"""
Simple test script for the Meeting Minutes Agent API
Run this after starting the server to test the endpoints
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_root():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_generate_minutes():
    """Test generating meeting minutes from text"""
    print("Testing generate minutes endpoint...")
    
    sample_transcript = """
    Meeting started at 10:00 AM.
    John discussed the new project timeline and mentioned we need to start next week.
    Sarah raised budget concerns and suggested we review the current allocation.
    Decision: Project will start next week as planned.
    Decision: Budget review meeting scheduled for Friday.
    Action: John to prepare detailed project plan by Friday.
    Action: Sarah to review and update budget spreadsheet by Monday.
    Meeting ended at 11:00 AM.
    """
    
    data = {"transcript": sample_transcript}
    response = requests.post(f"{BASE_URL}/generate-minutes", json=data)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("Meeting Minutes Generated:")
        print(f"Summary: {result['meeting_minutes'].get('summary', 'N/A')}")
        print(f"Decisions: {result['meeting_minutes'].get('decisions', [])}")
        print(f"Action Items: {result['meeting_minutes'].get('action_items', [])}")
    else:
        print(f"Error: {response.text}")
    print()

def main():
    """Run all tests"""
    print("=== Meeting Minutes Agent API Tests ===\n")
    
    try:
        test_root()
        test_health()
        test_generate_minutes()
        
        print("=== Tests Completed ===")
        print("Note: Audio transcription tests require actual audio files")
        print("You can test file uploads using tools like Postman or curl")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8000")
        print("Run: python main.py")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main()
