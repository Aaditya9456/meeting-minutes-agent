"use client"

import type React from "react"

import { useState, useCallback, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Upload, FileAudio, Download, Share2, Sparkles, Clock, Users, CheckCircle, AlertCircle, FileText, Copy, Check } from "lucide-react"
import { apiService, type MeetingMinutes, type ActionItem } from "@/lib/api"

interface ProcessedMeetingMinutes {
  title: string
  date: string
  duration: string
  participants: string[]
  keyPoints: string[]
  actionItems: string[]
  summary: string
  transcript: string
  decisions: string[]
  rawActionItems: ActionItem[]
}

interface ToastMessage {
  id: string
  message: string
  type: 'success' | 'error' | 'info'
}

export default function MeetingMinutesAI() {
  const [file, setFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [minutes, setMinutes] = useState<ProcessedMeetingMinutes | null>(null)
  const [dragActive, setDragActive] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showTranscript, setShowTranscript] = useState(false)
  const [toasts, setToasts] = useState<ToastMessage[]>([])
  const [copyStatus, setCopyStatus] = useState<'idle' | 'copying' | 'copied'>('idle')

  // Check API health on component mount
  useEffect(() => {
    checkAPIHealth()
  }, [])

  // Auto-remove toasts after 3 seconds
  useEffect(() => {
    if (toasts.length > 0) {
      const timer = setTimeout(() => {
        setToasts(prev => prev.slice(1))
      }, 3000)
      return () => clearTimeout(timer)
    }
  }, [toasts])

  const addToast = (message: string, type: 'success' | 'error' | 'info' = 'info') => {
    const id = Date.now().toString()
    setToasts(prev => [...prev, { id, message, type }])
  }

  const checkAPIHealth = async () => {
    try {
      await apiService.healthCheck()
      console.log('API is healthy')
    } catch (err) {
      console.error('API health check failed:', err)
      setError('Warning: Unable to connect to the API server. Please ensure the backend is running.')
    }
  }

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile.type.startsWith("audio/")) {
        setFile(droppedFile)
        setError(null)
      } else {
        setError("Please select an audio file (MP3, WAV, FLAC, etc.)")
      }
    }
  }, [])

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0]
      if (selectedFile.type.startsWith("audio/")) {
        setFile(selectedFile)
        setError(null)
      } else {
        setError("Please select an audio file (MP3, WAV, FLAC, etc.)")
      }
    }
  }

  const processAudio = async () => {
    if (!file) return

    setIsProcessing(true)
    setProgress(0)
    setError(null)

    // Start progress simulation
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval)
          return 90
        }
        return prev + Math.random() * 10
      })
    }, 300)
    try {

      // Call the API
      const result = await apiService.transcribeAndGenerateMinutes(file)
      
      clearInterval(progressInterval)
      setProgress(100)

      // Process the API response into our UI format
      const processedMinutes: ProcessedMeetingMinutes = {
        title: `Meeting - ${new Date().toLocaleDateString()}`,
        date: new Date().toLocaleDateString(),
        duration: "Processing time: ~2-3 minutes",
        participants: [], // We'll extract these from the transcript later if needed
        keyPoints: result.meeting_minutes.decisions || [],
        actionItems: result.meeting_minutes.action_items?.map(item => 
          `${item.task}${item.owner ? ` (${item.owner})` : ''}${item.due ? ` - Due: ${item.due}` : ''}`
        ) || [],
        summary: result.meeting_minutes.summary || "No summary generated",
        transcript: result.transcript,
        decisions: result.meeting_minutes.decisions || [],
        rawActionItems: result.meeting_minutes.action_items || []
      }

      setMinutes(processedMinutes)
      setIsProcessing(false)
      addToast('Meeting minutes generated successfully!', 'success')

    } catch (err: any) {
      clearInterval(progressInterval)
      setIsProcessing(false)
      setProgress(0)
      
      if (err.response?.data?.detail) {
        setError(`API Error: ${err.response.data.detail}`)
        addToast(`Error: ${err.response.data.detail}`, 'error')
      } else if (err.message) {
        setError(`Error: ${err.message}`)
        addToast(`Error: ${err.message}`, 'error')
      } else {
        setError('An unexpected error occurred while processing the audio file.')
        addToast('An unexpected error occurred while processing the audio file.', 'error')
      }
      
      console.error('Error processing audio:', err)
    }
  }

  const downloadMinutes = () => {
    if (!minutes) return

    const content = `
MEETING MINUTES
===============

Title: ${minutes.title}
Date: ${minutes.date}
Duration: ${minutes.duration}

TRANSCRIPT:
${minutes.transcript}

SUMMARY:
${minutes.summary}

KEY DECISIONS:
${minutes.decisions.map((d) => `• ${d}`).join("\n")}

ACTION ITEMS:
${minutes.rawActionItems.map((item) => 
  `• ${item.task}${item.owner ? ` (Owner: ${item.owner})` : ''}${item.due ? ` - Due: ${item.due}` : ''}`
).join("\n")}
    `.trim()

    const blob = new Blob([content], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `${minutes.title.replace(/\s+/g, "_")}_Minutes.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    addToast('Meeting minutes downloaded successfully!', 'success')
  }

  const copyToClipboard = async () => {
    if (!minutes) return
    
    setCopyStatus('copying')
    
    const content = `Meeting Summary: ${minutes.summary}\n\nKey Decisions: ${minutes.decisions.join(', ')}\n\nAction Items: ${minutes.actionItems.join(', ')}`
    
    try {
      await navigator.clipboard.writeText(content)
      setCopyStatus('copied')
      addToast('Meeting minutes copied to clipboard!', 'success')
      
      // Reset copy status after 2 seconds
      setTimeout(() => {
        setCopyStatus('idle')
      }, 2000)
      
    } catch (err) {
      console.error('Failed to copy to clipboard:', err)
      setCopyStatus('idle')
      addToast('Failed to copy to clipboard', 'error')
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Toast Notifications */}
      <div className="fixed top-4 right-4 z-50 space-y-2">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`px-4 py-3 rounded-lg shadow-lg max-w-sm transition-all duration-300 transform ${
              toast.type === 'success' 
                ? 'bg-green-500 text-white' 
                : toast.type === 'error' 
                ? 'bg-red-500 text-white' 
                : 'bg-blue-500 text-white'
            }`}
          >
            <div className="flex items-center gap-2">
              {toast.type === 'success' && <CheckCircle className="h-4 w-4" />}
              {toast.type === 'error' && <AlertCircle className="h-4 w-4" />}
              {toast.type === 'info' && <FileText className="h-4 w-4" />}
              <span className="text-sm font-medium">{toast.message}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Sparkles className="h-8 w-8 text-accent" />
            <h1 className="text-4xl font-bold text-foreground">Meeting Minutes Agent</h1>
          </div>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Transform your meeting recordings into structured, actionable minutes with the power of artificial intelligence
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <Card className="border-red-200 bg-red-50 mb-6">
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <AlertCircle className="h-5 w-5 text-red-500" />
                <p className="text-red-700">{error}</p>
              </div>
            </CardContent>
          </Card>
        )}

        {!minutes ? (
          <div className="space-y-8">
            {/* Upload Section */}
            <Card className="border-2 border-dashed border-border hover:border-accent/50 transition-colors">
              <CardHeader className="text-center">
                <CardTitle className="flex items-center justify-center gap-2">
                  <Upload className="h-5 w-5" />
                  Upload Meeting Audio
                </CardTitle>
                <CardDescription>
                  Drag and drop your audio file or click to browse. Supports MP3, WAV, FLAC, OGG, WebM formats.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div
                  className={`relative border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
                    dragActive ? "border-accent bg-accent/5" : "border-border hover:border-accent/50"
                  }`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  <input
                    type="file"
                    accept="audio/*"
                    onChange={handleFileChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  />

                  {file ? (
                    <div className="space-y-4">
                      <FileAudio className="h-12 w-12 text-accent mx-auto" />
                      <div>
                        <p className="font-medium text-foreground">{file.name}</p>
                        <p className="text-sm text-muted-foreground">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
                      </div>
                      <Badge variant="secondary" className="bg-accent/10 text-accent">
                        Ready to process
                      </Badge>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <Upload className="h-12 w-12 text-muted-foreground mx-auto" />
                      <div>
                        <p className="text-lg font-medium text-foreground">Drop your audio file here</p>
                        <p className="text-muted-foreground">or click to browse your files</p>
                      </div>
                    </div>
                  )}
                </div>

                {file && !isProcessing && (
                  <div className="mt-6 text-center">
                    <Button
                      onClick={processAudio}
                      size="lg"
                      className="bg-accent hover:bg-accent/90 text-accent-foreground"
                      disabled={!file}
                    >
                      <Sparkles className="h-4 w-4 mr-2" />
                      Generate Meeting Minutes
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Processing Section */}
            {isProcessing && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="h-5 w-5 text-accent animate-pulse" />
                    Processing Your Meeting
                  </CardTitle>
                  <CardDescription>
                    Our AI is analyzing your audio and generating structured meeting minutes...
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Progress value={progress} className="w-full" />
                  <div className="flex justify-between text-sm text-muted-foreground">
                    <span>Transcribing audio...</span>
                    <span>{Math.round(progress)}%</span>
                  </div>
                  <p className="text-xs text-muted-foreground text-center">
                    This may take 2-3 minutes depending on the audio length
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        ) : (
          /* Results Section */
          <div className="space-y-6">
            {/* Success Header */}
            <Card className="border-accent/20 bg-accent/5">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3 mb-2">
                  <CheckCircle className="h-6 w-6 text-accent" />
                  <h2 className="text-2xl font-bold text-foreground">Meeting Minutes Generated</h2>
                </div>
                <p className="text-muted-foreground">
                  Your meeting has been successfully processed and structured into actionable minutes.
                </p>
              </CardContent>
            </Card>

            {/* Meeting Info */}
            <Card>
              <CardHeader>
                <CardTitle>{minutes.title}</CardTitle>
                <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Clock className="h-4 w-4" />
                    {minutes.date} • {minutes.duration}
                  </div>
                  <div className="flex items-center gap-1">
                    <FileText className="h-4 w-4" />
                    {minutes.transcript.length} characters transcribed
                  </div>
                </div>
              </CardHeader>
            </Card>

            {/* Tabbed Content */}
            <Tabs defaultValue="summary" className="w-full">
              <TabsList className="grid w-full grid-cols-5">
                <TabsTrigger value="summary">Summary</TabsTrigger>
                <TabsTrigger value="decisions">Decisions</TabsTrigger>
                <TabsTrigger value="actions">Action Items</TabsTrigger>
                <TabsTrigger value="transcript">Transcript</TabsTrigger>
                <TabsTrigger value="raw">Raw Data</TabsTrigger>
              </TabsList>

              <TabsContent value="summary" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Meeting Summary</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Textarea value={minutes.summary} readOnly className="min-h-32 resize-none" />
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="decisions" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Key Decisions</CardTitle>
                  </CardHeader>
                  <CardContent>
                    {minutes.decisions.length > 0 ? (
                      <ul className="space-y-3">
                        {minutes.decisions.map((decision, index) => (
                          <li key={index} className="flex items-start gap-3">
                            <div className="h-2 w-2 rounded-full bg-accent mt-2 flex-shrink-0" />
                            <span className="text-foreground leading-relaxed">{decision}</span>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-muted-foreground">No decisions identified in this meeting.</p>
                    )}
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="actions" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Action Items</CardTitle>
                  </CardHeader>
                  <CardContent>
                    {minutes.rawActionItems.length > 0 ? (
                      <ul className="space-y-3">
                        {minutes.rawActionItems.map((item, index) => (
                          <li key={index} className="flex items-start gap-3">
                            <CheckCircle className="h-5 w-5 text-accent mt-0.5 flex-shrink-0" />
                            <div className="flex-1">
                              <span className="text-foreground leading-relaxed">{item.task}</span>
                              {(item.owner || item.due) && (
                                <div className="text-sm text-muted-foreground mt-1">
                                  {item.owner && <span className="mr-3">👤 {item.owner}</span>}
                                  {item.due && <span>📅 Due: {item.due}</span>}
                                </div>
                              )}
                            </div>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-muted-foreground">No action items identified in this meeting.</p>
                    )}
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="transcript" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Full Transcript</CardTitle>
                    <CardDescription>
                      The complete transcription of your meeting audio
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Textarea 
                      value={minutes.transcript} 
                      readOnly 
                      className="min-h-64 resize-none font-mono text-sm" 
                    />
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="raw" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Raw API Response</CardTitle>
                    <CardDescription>
                      The complete data structure returned by the API
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Textarea 
                      value={JSON.stringify(minutes, null, 2)} 
                      readOnly 
                      className="min-h-64 resize-none font-mono text-sm" 
                    />
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button onClick={downloadMinutes} size="lg" className="bg-accent hover:bg-accent/90">
                <Download className="h-4 w-4 mr-2" />
                Download Minutes
              </Button>
              <Button 
                onClick={copyToClipboard} 
                variant="outline" 
                size="lg"
                disabled={copyStatus === 'copying'}
                className={copyStatus === 'copied' ? 'bg-green-50 border-green-200 text-green-700' : ''}
              >
                {copyStatus === 'copying' ? (
                  <>
                    <div className="h-4 w-4 mr-2 animate-spin rounded-full border-2 border-current border-t-transparent" />
                    Copying...
                  </>
                ) : copyStatus === 'copied' ? (
                  <>
                    <Check className="h-4 w-4 mr-2" />
                    Copied!
                  </>
                  ) : (
                  <>
                    <Copy className="h-4 w-4 mr-2" />
                    Copy to Clipboard
                  </>
                )}
              </Button>
              <Button
                variant="ghost"
                size="lg"
                onClick={() => {
                  setFile(null)
                  setMinutes(null)
                  setProgress(0)
                  setError(null)
                }}
              >
                Process Another Meeting
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
