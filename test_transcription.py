#!/usr/bin/env python3
"""
Test script for the transcription function
"""

import os
from dotenv import load_dotenv
from transcription import transcribe_audio

def test_transcription():
    """Test the transcription function"""
    print("🧪 Testing Transcription Function")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check if HF_TOKEN is available
    if "HF_TOKEN" not in os.environ:
        print("❌ HF_TOKEN not found in environment variables")
        print("Please set HF_TOKEN in your .env file")
        return False
    
    print("✅ HF_TOKEN found")
    
    # Test with a sample file if it exists
    test_files = ["sample1.flac", "sample1.wav", "sample1.mp3"]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📁 Testing with file: {test_file}")
            print(f"📊 File size: {os.path.getsize(test_file) / 1024:.1f} KB")
            
            try:
                result = transcribe_audio(test_file)
                print(f"✅ Transcription successful!")
                print(f"📝 Result type: {type(result)}")
                print(f"📝 Result: {result}")
                
                if result and isinstance(result, str):
                    print(f"📊 Character count: {len(result)}")
                    return True
                else:
                    print("❌ Result is not a valid string")
                    return False
                    
            except Exception as e:
                print(f"❌ Transcription failed: {e}")
                return False
    
    print("\n❌ No test files found")
    print("Please create a sample audio file (sample1.flac, sample1.wav, or sample1.mp3)")
    return False

if __name__ == "__main__":
    success = test_transcription()
    if success:
        print("\n🎉 Transcription test passed!")
    else:
        print("\n💥 Transcription test failed!")
        print("Check your HF_TOKEN and try again")
