# 🚀 Meeting Minutes Agent - Complete Demo

A full-stack application that combines **FastAPI backend** with **Next.js frontend** to create an AI-powered meeting minutes generator.

## ✨ Features

- **🎵 Audio Transcription**: Upload audio files (MP3, WAV, FLAC, OGG, WebM)
- **🤖 AI Meeting Minutes**: Generate structured summaries, decisions, and action items
- **🌐 Modern Web UI**: Beautiful, responsive Next.js interface
- **🔧 RESTful API**: FastAPI backend with comprehensive endpoints
- **📱 Drag & Drop**: Easy file upload with visual feedback
- **📊 Progress Tracking**: Real-time processing status
- **💾 Export Options**: Download minutes as text files
- **📋 Copy to Clipboard**: Quick sharing functionality

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js UI   │    │   FastAPI       │    │   External      │
│   (Frontend)   │◄──►│   (Backend)     │◄──►│   APIs          │
│                 │    │                 │    │                 │
│ • File Upload  │    │ • Audio         │    │ • Hugging Face  │
│ • Progress Bar │    │   Processing    │    │   (Transcription)│
│ • Results      │    │ • Meeting       │    │ • OpenAI        │
│   Display      │    │   Minutes Gen   │    │   (AI Agent)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+** with `uv` package manager
- **Node.js 18+** with `npm`
- **API Keys**: Hugging Face token and OpenAI API key

### 1. Clone and Setup

```bash
# Navigate to project directory
cd meeting-minutes-agent

# Install Python dependencies
uv sync

# Install frontend dependencies
cd meeing_minutes_agent
npm install
cd ..
```

### 2. Configure Environment

```bash
# Copy environment templates
cp env_template.txt .env
cp meeing_minutes_agent/env_frontend.txt meeing_minutes_agent/.env.local

# Edit .env with your API keys
HF_TOKEN=your_huggingface_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Start the Complete Demo

```bash
# One command to start everything!
python start_demo.py
```

This will:
- ✅ Start FastAPI backend on port 8000
- ✅ Start Next.js frontend on port 3000
- ✅ Open your browser automatically
- ✅ Provide health checks and status

### 4. Manual Startup (Alternative)

```bash
# Terminal 1: Start backend
python main.py

# Terminal 2: Start frontend
cd meeing_minutes_agent
npm run dev
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📱 How to Use

### 1. Upload Audio
- Drag & drop an audio file or click to browse
- Supported formats: MP3, WAV, FLAC, OGG, WebM
- File size limit: 50MB

### 2. Process Meeting
- Click "Generate Meeting Minutes"
- Watch real-time progress updates
- Processing takes 2-3 minutes for typical meetings

### 3. View Results
- **Summary**: AI-generated meeting overview
- **Decisions**: Key decisions made during the meeting
- **Action Items**: Tasks with owners and due dates
- **Transcript**: Full audio transcription
- **Raw Data**: Complete API response

### 4. Export & Share
- Download minutes as text file
- Copy summary to clipboard
- Process another meeting

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and endpoints |
| `/health` | GET | Health check and configuration |
| `/transcribe` | POST | Upload audio + generate minutes |
| `/transcribe-only` | POST | Upload audio for transcription only |
| `/generate-minutes` | POST | Generate minutes from text |

## 🛠️ Development

### Backend Development

```bash
# Run with auto-reload
DEBUG=True python main.py

# Test API endpoints
python test_api.py

# Check individual components
python transcription.py
python agent.py
```

### Frontend Development

```bash
cd meeing_minutes_agent

# Development mode
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### Adding Features

1. **New API Endpoints**: Add to `main.py`
2. **New UI Components**: Add to `meeing_minutes_agent/components/`
3. **API Integration**: Update `meeing_minutes_agent/lib/api.ts`
4. **Styling**: Modify `meeing_minutes_agent/app/globals.css`

## 🧪 Testing

### Backend Testing

```bash
# Test API endpoints
python test_api.py

# Test individual components
python transcription.py
python agent.py
```

### Frontend Testing

```bash
cd meeing_minutes_agent

# Run tests (if configured)
npm test

# Lint code
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
- [ ] Prepare sample audio files
- [ ] Test different audio formats

**Happy Demo-ing! 🚀**
