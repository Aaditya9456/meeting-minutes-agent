import os
from huggingface_hub import InferenceClient

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe audio file using Hugging Face inference API
    
    Args:
        audio_file_path (str): Path to the audio file
        
    Returns:
        str: Transcribed text
    """
    try:
        # Check if HF_TOKEN is available
        if "HF_TOKEN" not in os.environ:
            raise ValueError("HF_TOKEN environment variable not found")
        
        client = InferenceClient(
            provider="fal-ai",
            api_key=os.environ["HF_TOKEN"],
        )
        
        # Transcribe the audio file
        output = client.automatic_speech_recognition(
            audio_file_path, 
            model="openai/whisper-large-v3"
        )
        print(output)
        
        # Handle different response types
        if hasattr(output, 'text'):
            # If it's an object with a text attribute
            return output.text
        elif isinstance(output, dict) and 'text' in output:
            # If it's a dictionary with text key
            return output['text']
        elif isinstance(output, str):
            # If it's already a string
            return output
        elif hasattr(output, '__str__'):
            # Try to convert to string as fallback
            return str(output)
        else:
            # Last resort - try to access common attributes
            print(f"Unexpected output type: {type(output)}")
            print(f"Output content: {output}")
            return "Transcription completed but text extraction failed"
        
    except Exception as e:
        print(f"Error in transcription: {str(e)}")
        return None

# For testing purposes
if __name__ == "__main__":
    # Test with a sample file if it exists
    test_file = "sample1.flac"
    if os.path.exists(test_file):
        result = transcribe_audio(test_file)
        print(f"Transcription result: {result}")
        print(f"Result type: {type(result)}")
    else:
        print(f"Test file {test_file} not found")
