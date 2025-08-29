# 🚀 Meeting Minutes Agent

A full-stack AI-powered application that transforms meeting recordings into structured, actionable minutes. Built with **FastAPI backend** and **Next.js frontend**.

## ✨ Features

- **🎵 Audio Transcription**: Upload audio files (MP3, WAV, FLAC, OGG, WebM) using Hugging Face Whisper
- **🤖 AI Meeting Minutes**: Generate structured summaries, decisions, and action items using OpenAI Agent SDK
- **🌐 Modern Web UI**: Beautiful, responsive Next.js interface with drag & drop file upload
- **🔧 RESTful API**: FastAPI backend with comprehensive endpoints and validation
- **📱 Drag & Drop**: Easy file upload with visual feedback and progress tracking
- **📊 Real-time Progress**: Live processing status updates during transcription
- **💾 Export Options**: Download minutes as text files or copy to clipboard
- **🎨 Toast Notifications**: Professional feedback system for all user actions

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js UI   │    │   FastAPI       │    │   External      │
│   (Frontend)   │◄──►│   (Backend)     │◄──►│   APIs          │
│                 │    │                 │    │                 │
│ • File Upload  │    │ • Audio         │    │ • Hugging Face  │
│ • Progress Bar │    │   Processing    │    │   (Whisper v3)  │
│ • Results      │    │ • Meeting       │    │ • OpenAI        │
│   Display      │    │   Minutes Gen   │    │   (Agent SDK)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+** with `uv` package manager
- **Node.js 18+** with `npm`
- **API Keys**: 
  - Hugging Face token (for audio transcription)
  - OpenAI API key (for meeting minutes generation)

### 1. Setup Environment

```bash
# Copy environment templates
cp env_template.txt .env
cp meeing_minutes_agent/env_frontend.txt meeing_minutes_agent/.env.local

# Edit .env with your API keys
HF_TOKEN=your_huggingface_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Install Dependencies

```bash
# Backend dependencies
uv sync

# Frontend dependencies
cd meeing_minutes_agent
npm install
cd ..
```

### 3. Start the Application

#### Option A: One Command (Recommended)
```bash
python start_demo.py
```

#### Option B: Manual Startup
```bash
# Terminal 1: Start FastAPI backend
python main.py

# Terminal 2: Start Next.js frontend
cd meeing_minutes_agent
npm run dev
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📱 How to Use

### 1. Upload Audio
- Drag & drop an audio file or click to browse
- Supported formats: MP3, WAV, FLAC, OGG, WebM
- File size limit: 50MB (configurable)

### 2. Process Meeting
- Click "Generate Meeting Minutes"
- Watch real-time progress updates
- Processing takes 2-3 minutes for typical meetings

### 3. View Results
- **Summary**: AI-generated meeting overview
- **Decisions**: Key decisions made during the meeting
- **Action Items**: Tasks with owners and due dates
- **Transcript**: Full audio transcription
- **Raw Data**: Complete API response for debugging

### 4. Export & Share
- Download minutes as text file
- Copy summary to clipboard with visual feedback
- Process another meeting

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and available endpoints |
| `/health` | GET | Health check and configuration status |
| `/transcribe` | POST | Upload audio file and generate meeting minutes |
| `/transcribe-only` | POST | Upload audio file for transcription only |
| `/generate-minutes` | POST | Generate meeting minutes from existing transcript text |

## 🛠️ Development

### Backend Development (FastAPI)

```bash
# Run with auto-reload
DEBUG=True python main.py

# Test API endpoints
python test_api.py

# Test individual components
python transcription.py
python agent.py

# Test transcription function
python test_transcription.py
```

### Frontend Development (Next.js)

```bash
cd meeing_minutes_agent

# Development mode
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

### Adding New Features

1. **New API Endpoints**: Add to `main.py`
2. **New UI Components**: Add to `meeing_minutes_agent/components/`
3. **API Integration**: Update `meeing_minutes_agent/lib/api.ts`
4. **Styling**: Modify `meeing_minutes_agent/app/globals.css`

## 🧪 Testing

### Backend Testing
```bash
# Test API endpoints
python test_api.py

# Test transcription
python test_transcription.py

# Test individual components
python transcription.py
python agent.py
```

### Frontend Testing
```bash
cd meeing_minutes_agent
npm run lint
```

### Integration Testing
1. Start both servers
2. Upload an audio file through the UI
3. Verify transcription and meeting minutes generation
4. Check all UI tabs display correctly

## 🚨 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| **Backend won't start** | Check `.env` file and API keys |
| **Frontend won't start** | Run `npm install` in frontend directory |
| **Audio processing fails** | Verify Hugging Face token and file format |
| **Meeting minutes empty** | Check OpenAI API key and quota |
| **CORS errors** | Ensure backend is running on port 8000 |
| **Transcription errors** | Check audio file format and size |

### Debug Mode

```bash
# Backend debug
DEBUG=True python main.py

# Frontend debug
cd meeing_minutes_agent
npm run dev
```

### Logs

- **Backend**: Check terminal output for FastAPI logs
- **Frontend**: Check browser console for React logs
- **API Calls**: Monitor Network tab in browser dev tools

## 🔒 Security & Production

### Current State
- ✅ Basic file validation
- ✅ File size limits
- ✅ Error handling
- ✅ CORS configuration
- ⚠️ No authentication
- ⚠️ No rate limiting

### Production Considerations
- Add user authentication
- Implement rate limiting
- Add file storage (S3, etc.)
- Enable HTTPS
- Add monitoring and logging
- Set up CI/CD pipeline

## 📈 Performance

- **Audio Processing**: 2-3 minutes for typical meetings
- **File Size Limit**: 50MB (configurable)
- **Supported Formats**: MP3, WAV, FLAC, OGG, WebM
- **Concurrent Users**: Single instance (add load balancing for scale)

## 📁 Project Structure

```
meeting-minutes-agent/
├── main.py                      # FastAPI server and endpoints
├── config.py                    # Configuration management
├── transcription.py             # Audio transcription logic
├── agent.py                     # Meeting minutes generation
├── test_api.py                  # API testing script
├── test_transcription.py        # Transcription testing script
├── start_demo.py                # Complete demo startup script
├── env_template.txt             # Environment variables template
├── pyproject.toml               # Python dependencies
├── meeing_minutes_agent/        # Next.js frontend
│   ├── app/                     # Next.js app directory
│   │   ├── page.tsx            # Main application page
│   │   ├── layout.tsx          # App layout
│   │   └── globals.css         # Global styles
│   ├── components/              # UI components
│   │   └── ui/                 # Shadcn/ui components
│   ├── lib/                     # Utility functions
│   │   └── api.ts              # API service layer
│   ├── package.json             # Node.js dependencies
│   └── env_frontend.txt        # Frontend environment template
├── README.md                    # This file
└── README_DEMO.md              # Comprehensive demo guide
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

## 🆘 Support

- **Issues**: Check the troubleshooting section above
- **API Docs**: Visit http://localhost:8000/docs
- **Backend Logs**: Check terminal output
- **Frontend Logs**: Check browser console

---

## 🎯 Demo Checklist

Before presenting:

- [ ] Both servers are running
- [ ] API keys are configured
- [ ] Test with a sample audio file
- [ ] Verify all UI tabs work
- [ ] Test download functionality
- [ ] Check error handling
- [ ] Test copy to clipboard
- [ ] Prepare sample audio files
- [ ] Test different audio formats

**Happy Demo-ing! 🚀**
