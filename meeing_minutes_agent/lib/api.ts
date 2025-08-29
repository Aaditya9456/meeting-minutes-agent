import axios from 'axios';

// API base URL - change this to match your FastAPI server
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes for audio processing
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types for API responses
export interface ActionItem {
  task: string;
  owner?: string;
  due?: string;
}

export interface MeetingMinutes {
  summary: string;
  decisions: string[];
  action_items: ActionItem[];
}

export interface TranscriptResponse {
  transcript: string;
  meeting_minutes: MeetingMinutes;
  success: boolean;
  message: string;
}

export interface TranscribeOnlyResponse {
  transcript: string;
  success: boolean;
  message: string;
}

// API functions
export const apiService = {
  // Transcribe audio and generate meeting minutes
  async transcribeAndGenerateMinutes(file: File): Promise<TranscriptResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('generate_minutes', 'true');

    const response = await api.post<TranscriptResponse>('/transcribe', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Transcribe audio only
  async transcribeOnly(file: File): Promise<TranscribeOnlyResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<TranscribeOnlyResponse>('/transcribe-only', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Generate meeting minutes from transcript text
  async generateMinutesFromText(transcript: string): Promise<TranscriptResponse> {
    const response = await api.post<TranscriptResponse>('/generate-minutes', {
      transcript,
    });
    return response.data;
  },

  // Health check
  async healthCheck() {
    const response = await api.get('/health');
    return response.data;
  },
};

export default apiService;
