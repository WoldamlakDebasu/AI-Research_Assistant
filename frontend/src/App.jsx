import { useState, useEffect, useRef } from 'react'
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { Search, Brain, FileText, Loader2, CheckCircle, AlertCircle, Download } from 'lucide-react'
import io from 'socket.io-client'
import jsPDF from 'jspdf'
import { marked } from "marked";
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
import html2canvas from 'html2canvas'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [isResearching, setIsResearching] = useState(false)
  const [taskId, setTaskId] = useState(null)
  const [thoughts, setThoughts] = useState([])
  const [progress, setProgress] = useState(0)
  const [report, setReport] = useState('')
  const [status, setStatus] = useState('idle')
  const [error, setError] = useState('')
  
  const socketRef = useRef(null)
  const thoughtsEndRef = useRef(null)

  const downloadReport = async () => {
    if (!report) return;
    const pdf = new jsPDF('p', 'mm', 'a4');
    // Convert markdown to HTML
    const html = marked(report);
    // Create a temporary element to render HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    document.body.appendChild(tempDiv);
    // Use html2canvas to render the HTML to canvas
    const canvas = await html2canvas(tempDiv, { backgroundColor: '#fff' });
    const imgData = canvas.toDataURL('image/png');
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const canvasWidth = canvas.width;
    const canvasHeight = canvas.height;
    const ratio = canvasWidth / canvasHeight;
    const width = pdfWidth;
    const height = width / ratio;
    pdf.addImage(imgData, 'PNG', 0, 0, width, height);
    pdf.save(`research-report-${taskId || 'local'}.pdf`);
    document.body.removeChild(tempDiv);
  };

  const scrollToBottom = () => {
    thoughtsEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [thoughts])

  const connectSocket = (taskId) => {
      socketRef.current = io(BACKEND_URL);
    
    socketRef.current.on('connect', () => {
      console.log('Connected to server')
      socketRef.current.emit('join_task', { task_id: taskId })
    })

    socketRef.current.on('thought', (data) => {
      if (data.task_id === taskId) {
        setThoughts(prev => [...prev, data.thought])
      }
    })

    socketRef.current.on('progress', (data) => {
      if (data.task_id === taskId) {
        setProgress(data.progress)
      }
    })

    socketRef.current.on('report_complete', (data) => {
      if (data.task_id === taskId) {
        setReport(data.report)
        setStatus('completed')
        setIsResearching(false)
      }
    })

    socketRef.current.on('error', (data) => {
      if (data.task_id === taskId) {
        setError(data.error)
        setStatus('error')
        setIsResearching(false)
      }
    })

    socketRef.current.on('disconnect', () => {
      console.log('Disconnected from server')
    })
  }

  const disconnectSocket = () => {
    if (socketRef.current) {
      socketRef.current.disconnect()
      socketRef.current = null
    }
  }

  const startResearch = async () => {
    if (!query.trim()) return

    setIsResearching(true)
    setThoughts([])
    setProgress(0)
    setReport('')
    setStatus('starting')
    setError('')

    try {
        const response = await fetch(`${BACKEND_URL}/api/research`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query.trim() }),
      })

      if (!response.ok) {
        throw new Error('Failed to start research')
      }

      const data = await response.json()
      setTaskId(data.task_id)
      setStatus('running')
      connectSocket(data.task_id)

    } catch (err) {
      setError(err.message)
      setStatus('error')
      setIsResearching(false)
    }
  }

  const resetResearch = () => {
    disconnectSocket()
    setQuery('')
    setIsResearching(false)
    setTaskId(null)
    setThoughts([])
    setProgress(0)
    setReport('')
    setStatus('idle')
    setError('')
  }

  const getStatusIcon = () => {
    switch (status) {
      case 'running':
        return <Loader2 className="h-4 w-4 animate-spin" />
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-500" />
      default:
        return <Brain className="h-4 w-4" />
    }
  }

  const getStatusText = () => {
    switch (status) {
      case 'starting':
        return 'Initializing...'
      case 'running':
        return 'Researching...'
      case 'completed':
        return 'Research Complete'
      case 'error':
        return 'Error Occurred'
      default:
        return 'Ready'
    }
  }

  return (
    <div className="min-h-screen overflow-y-auto bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-gray-900 flex items-center justify-center gap-2">
            <Brain className="h-8 w-8 text-blue-600" />
            AI Research Agent
          </h1>
          <p className="text-lg text-gray-600">
            Multi-Step Autonomous Research with Real-Time Insights
          </p>
        </div>

        {/* Input Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="h-5 w-5" />
              Research Query
            </CardTitle>
            <CardDescription>
              Enter a complex research question and watch the AI agent break it down, search, and compile a comprehensive report.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-2">
              <Input
                placeholder="e.g., Generate a report on the market trends for lab-grown diamonds, including key players, recent funding, and technological challenges."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled={isResearching}
                className="flex-1"
                onKeyPress={(e) => e.key === 'Enter' && !isResearching && startResearch()}
              />
              <Button 
                onClick={startResearch} 
                disabled={isResearching || !query.trim()}
                className="px-6"
              >
                {isResearching ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Researching
                  </>
                ) : (
                  <>
                    <Search className="h-4 w-4 mr-2" />
                    Start Research
                  </>
                )}
              </Button>
            </div>
            
            {/* Status and Progress */}
            {(isResearching || status !== 'idle') && (
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    {getStatusIcon()}
                    <span className="text-sm font-medium">{getStatusText()}</span>
                    {taskId && (
                      <Badge variant="outline" className="text-xs">
                        Task: {taskId.slice(0, 8)}...
                      </Badge>
                    )}
                  </div>
                  {status === 'completed' && (
                    <Button variant="outline" size="sm" onClick={resetResearch}>
                      New Research
                    </Button>
                  )}
                </div>
                {isResearching && (
                  <Progress value={progress} className="w-full" />
                )}
              </div>
            )}

            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Main Content Grid - Responsive */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Agent Thoughts */}
          <Card className="h-96">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Brain className="h-5 w-5" />
                Agent Thoughts
                {thoughts.length > 0 && (
                  <Badge variant="secondary">{thoughts.length}</Badge>
                )}
              </CardTitle>
              <CardDescription>
                Real-time updates on what the AI agent is thinking and doing
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-64">
                <div className="space-y-2">
                  {thoughts.length === 0 ? (
                    <p className="text-sm text-gray-500 italic">
                      Agent thoughts will appear here during research...
                    </p>
                  ) : (
                    thoughts.map((thought, index) => (
                      <div key={index} className="flex items-start gap-2 p-2 bg-gray-50 rounded-md">
                        <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0" />
                        <p className="text-sm text-gray-700">{thought}</p>
                      </div>
                    ))
                  )}
                  <div ref={thoughtsEndRef} />
                </div>
              </ScrollArea>
            </CardContent>
          </Card>

          {/* Research Report */}
          <Card className="h-96">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Research Report
                </div>
                {report && (
                  <Button variant="outline" size="sm" onClick={downloadReport}>
                    <Download className="h-4 w-4 mr-2" />
                    Download PDF
                  </Button>
                )}
              </CardTitle>
              <CardDescription>
                Compiled findings and analysis from the research process
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-64 overflow-y-auto">
                {report ? (
                  <div id="report-content" className="prose prose-sm max-w-none">
                    <div dangerouslySetInnerHTML={{ __html: marked(report) }} />
                  </div>
                ) : (
                  <p className="text-sm text-gray-500 italic">
                    Research report will appear here when completed...
                  </p>
                )}
              </ScrollArea>
            </CardContent>
          </Card>
        </div>

        {/* Demo Examples */}
        <Card>
          <CardHeader>
            <CardTitle>Example Research Queries</CardTitle>
            <CardDescription>
              Try these sample queries to see the AI research agent in action
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-1 gap-4">
              {[
                "Analyze the current state of electric vehicle adoption in Europe, including market leaders and charging infrastructure challenges",
                "Research the impact of AI on healthcare diagnostics, including key companies, recent breakthroughs, and regulatory considerations",
                "Investigate the renewable energy storage market, focusing on battery technologies, major players, and investment trends",
                "Examine the future of remote work technology, including collaboration tools, security challenges, and market opportunities"
              ].map((example, index) => (
                <Button
                  key={index}
                  variant="outline"
                  className="h-auto p-4 text-left justify-start"
                  onClick={() => !isResearching && setQuery(example)}
                  disabled={isResearching}
                >
                  <div className="text-sm">{example}</div>
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default App

