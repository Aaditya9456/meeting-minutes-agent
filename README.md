# Meeting Minutes Agent API

A FastAPI server that combines audio transcription (using Hugging Face) and meeting minutes generation (using OpenAI Agent SDK).

## Features

- **Audio Transcription**: Upload audio files and get text transcripts
- **Meeting Minutes Generation**: Generate structured meeting minutes from transcripts
- **Combined Workflow**: Upload audio → Transcribe → Generate meeting minutes in one request
- **Flexible API**: Use individual endpoints or combined workflow
- **File Validation**: Supports multiple audio formats with size limits
- **Environment-based Configuration**: Easy configuration via environment variables

## API Endpoints

- `GET /` - API information and available endpoints
- `GET /health` - Health check and configuration status
- `POST /transcribe` - Upload audio file and optionally generate meeting minutes
- `POST /transcribe-only` - Upload audio file for transcription only
- `POST /generate-minutes` - Generate meeting minutes from existing transcript text

## Quick Start

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy the template and fill in your API keys:

```bash
cp env_template.txt .env
```

Edit `.env` with your actual values:

```env
# Required API Keys
HF_TOKEN=your_huggingface_token_here
OPENAI_API_KEY=your_openai_api_key_here

# Optional Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 3. Run the Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### 4. Test the API

```bash
python test_api.py
```

Or visit `http://localhost:8000/docs` for interactive API documentation.

## Usage Examples

### Generate Meeting Minutes from Text

```bash
curl -X POST "http://localhost:8000/generate-minutes" \
     -H "Content-Type: application/json" \
     -d '{
       "transcript": "Meeting started at 10:00 AM. John discussed project timeline..."
     }'
```

### Upload Audio and Generate Minutes

```bash
curl -X POST "http://localhost:8000/transcribe" \
     -F "file=@meeting_recording.wav" \
     -F "generate_minutes=true"
```

### Transcribe Audio Only

```bash
curl -X POST "http://localhost:8000/transcribe-only" \
     -F "file=@meeting_recording.mp3"
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `HF_TOKEN` | Hugging Face API token | - | Yes |
| `OPENAI_API_KEY` | OpenAI API key | - | Yes |
| `HOST` | Server host | `0.0.0.0` | No |
| `PORT` | Server port | `8000` | No |
| `DEBUG` | Debug mode | `False` | No |
| `MAX_FILE_SIZE` | Maximum file size (bytes) | `52428800` (50MB) | No |
| `TRANSCRIPTION_MODEL` | Whisper model to use | `openai/whisper-large-v3` | No |

### Supported Audio Formats

- WAV (.wav)
- MP3 (.mp3, .mpeg)
- FLAC (.flac)
- OGG (.ogg)
- WebM (.webm)

## Project Structure

```
meeting-minutes-agent/
├── main.py              # FastAPI server and endpoints
├── config.py            # Configuration management
├── transcription.py     # Audio transcription logic
├── agent.py            # Meeting minutes generation
├── test_api.py         # API testing script
├── env_template.txt    # Environment variables template
├── pyproject.toml      # Project dependencies
└── README.md           # This file
```

## Development

### Running in Development Mode

```bash
DEBUG=True python main.py
```

### Testing

```bash
# Test the API endpoints
python test_api.py

# Test individual components
python transcription.py
python agent.py
```

### Adding New Features

1. **New Endpoints**: Add to `main.py`
2. **New Models**: Update Pydantic models in respective files
3. **Configuration**: Add to `config.py`
4. **Testing**: Update `test_api.py`

## Troubleshooting

### Common Issues

1. **Missing API Keys**: Ensure `HF_TOKEN` and `OPENAI_API_KEY` are set in `.env`
2. **File Upload Errors**: Check file format and size limits
3. **Transcription Failures**: Verify Hugging Face token and model availability
4. **Agent Errors**: Check OpenAI API key and quota

### Debug Mode

Enable debug mode to see detailed error messages:

```bash
DEBUG=True python main.py
```

## Next Steps

- [ ] Add authentication and rate limiting
- [ ] Implement file storage and management
- [ ] Add support for multiple meeting formats
- [ ] Create web UI for easier interaction
- [ ] Add batch processing capabilities
- [ ] Implement caching for better performance

## License

This project is open source. Feel free to contribute and improve!
