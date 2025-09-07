# Quick Setup Guide

## Prerequisites

1. **Python 3.11+** installed
2. **Node.js 20+** installed
3. **OpenAI API Key** (set as environment variable `OPENAI_API_KEY`)

## Installation Steps

### 1. Extract the Project
```bash
unzip research-agent-demo.zip
cd research-agent-demo
```

### 2. Setup Backend
```bash
cd research-agent-backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup Frontend
```bash
cd ../research-agent-frontend
npm install  # or pnpm install
```

### 4. Set Environment Variables
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### 5. Start the Application

**Terminal 1 - Backend:**
```bash
cd research-agent-backend
source venv/bin/activate
python src/main.py
```

**Terminal 2 - Frontend:**
```bash
cd research-agent-frontend
npm run dev  # or pnpm run dev
```

### 6. Open Browser
Navigate to: http://localhost:5173

## Testing the Demo

1. Enter a research query like: "Analyze the electric vehicle market in Europe"
2. Click "Start Research"
3. Watch the real-time agent thoughts appear
4. Wait for the research report to be generated

## Troubleshooting

### Common Issues

**Backend won't start:**
- Check Python version: `python --version`
- Ensure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`

**Frontend won't start:**
- Check Node.js version: `node --version`
- Clear cache: `npm cache clean --force`
- Reinstall dependencies: `rm -rf node_modules && npm install`

**OpenAI API Errors:**
- Verify API key is set: `echo $OPENAI_API_KEY`
- Check API key permissions and credits
- Ensure internet connection for API calls

**WebSocket Connection Issues:**
- Ensure backend is running on port 5000
- Check firewall settings
- Try refreshing the browser page

### Port Configuration

If you need to change ports:

**Backend (default: 5000):**
Edit `research-agent-backend/src/main.py`, line 73:
```python
socketio.run(app, host='0.0.0.0', port=YOUR_PORT, debug=True)
```

**Frontend (default: 5173):**
Edit `research-agent-frontend/vite.config.js`:
```javascript
export default defineConfig({
  server: {
    port: YOUR_PORT
  }
})
```

Also update the backend URL in `research-agent-frontend/src/App.jsx`:
```javascript
const response = await fetch('http://localhost:YOUR_BACKEND_PORT/api/research', {
```

## Demo Script for Clients

### 1. Introduction (30 seconds)
"This is an autonomous AI research agent that can handle complex research tasks automatically. Unlike simple chatbots, this system can plan, search the web, analyze content, and generate comprehensive reports."

### 2. Query Input (30 seconds)
"Let me enter a complex research query that would normally take hours of manual work..."
[Enter: "Generate a report on the market trends for lab-grown diamonds, including key players, recent funding, and technological challenges"]

### 3. Real-Time Process (2-3 minutes)
"Watch as the AI agent breaks down this complex query, performs web searches, scrapes content from multiple sources, and compiles everything into a structured report. You can see its thinking process in real-time."

### 4. Results Review (1 minute)
"The system has generated a comprehensive research report with market analysis, key players, funding information, and technological challenges - all automatically sourced from current web data."

### 5. Business Value (1 minute)
"This demonstrates how we can automate knowledge work, reduce research time from hours to minutes, and scale intelligence across your organization. The system can be customized for your specific industry and data sources."

## Next Steps

1. **Evaluate the Demo**: Test with your own research queries
2. **Discuss Customization**: How to adapt for your specific needs
3. **Plan Integration**: How to incorporate into your existing workflows
4. **Consider Deployment**: Cloud hosting and scaling options

## Contact

For questions about customization, deployment, or licensing, please reach out to discuss your specific requirements.

