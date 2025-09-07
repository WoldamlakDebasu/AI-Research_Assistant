# AI Research Agent Demo

## Overview

This is a professional multi-step AI research agent demo that showcases autonomous research capabilities with real-time insights. The system demonstrates advanced agentic AI functionality that goes beyond simple Q&A, featuring planning, tool use, web search, web scraping, and state management.

## Features

- **Multi-Step Research Process**: Automatically breaks down complex queries into sub-questions
- **Real-Time Agent Thoughts**: Live updates showing what the AI agent is thinking and doing
- **Web Search Integration**: Uses DuckDuckGo and Bing search engines to find relevant information
- **Intelligent Web Scraping**: Extracts content from web pages and summarizes findings
- **Report Generation**: Compiles research findings into structured, professional reports
- **WebSocket Communication**: Real-time updates between frontend and backend
- **Professional UI**: Clean, modern interface built with React and Tailwind CSS
- **Progress Tracking**: Visual progress indicators and status updates

## Architecture

### Backend (Flask API)
- **Flask Application**: RESTful API with WebSocket support
- **Research Agent**: Core logic for query breakdown and research orchestration
- **Search Engine**: Integration with DuckDuckGo and Bing for web search
- **Web Scraper**: Intelligent content extraction from web pages
- **OpenAI Integration**: Uses GPT models for query analysis and content summarization

### Frontend (React Application)
- **Modern React UI**: Built with Vite, Tailwind CSS, and shadcn/ui components
- **Real-Time Updates**: WebSocket client for live agent thoughts and progress
- **Responsive Design**: Works on desktop and mobile devices
- **Professional Styling**: Clean, business-ready interface

## Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- OpenAI API key (set as environment variable)

### Backend Setup
```bash
cd research-agent-backend
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

### Frontend Setup
```bash
cd research-agent-frontend
pnpm install
pnpm run dev --host
```

## Usage

1. **Start the Backend**: Run the Flask server on port 5000
2. **Start the Frontend**: Run the React development server on port 5173
3. **Open Browser**: Navigate to http://localhost:5173
4. **Enter Query**: Type a complex research question in the input field
5. **Watch Magic Happen**: Observe real-time agent thoughts and research process
6. **Review Report**: Read the compiled research report when complete

### Example Queries
- "Generate a report on the market trends for lab-grown diamonds, including key players, recent funding, and technological challenges"
- "Analyze the current state of electric vehicle adoption in Europe, including market leaders and charging infrastructure challenges"
- "Research the impact of AI on healthcare diagnostics, including key companies, recent breakthroughs, and regulatory considerations"

## Technical Implementation

### Research Process Flow
1. **Query Analysis**: AI breaks down the main query into 3-5 sub-questions
2. **Web Search**: Each sub-question is searched using multiple search engines
3. **Content Scraping**: Top 3 results for each search are scraped for content
4. **Content Summarization**: Scraped content is summarized using AI
5. **Report Compilation**: All findings are compiled into a structured report
6. **Real-Time Updates**: Progress and thoughts are streamed to the frontend

### Key Technologies
- **Backend**: Flask, Flask-SocketIO, OpenAI, BeautifulSoup, Requests
- **Frontend**: React, Vite, Tailwind CSS, shadcn/ui, Socket.IO Client
- **Communication**: WebSocket for real-time updates, REST API for commands
- **Search**: DuckDuckGo and Bing search integration
- **AI**: OpenAI GPT models for analysis and summarization

## API Endpoints

### POST /api/research
Start a new research task
- **Body**: `{ "query": "research question" }`
- **Response**: `{ "task_id": "uuid" }`

### GET /api/status/<task_id>
Get research task status
- **Response**: `{ "status": "running", "thoughts": [...], "report": "...", "progress": 75 }`

### WebSocket Events
- **join_task**: Join a task room for real-time updates
- **thought**: Receive agent thoughts
- **progress**: Receive progress updates
- **report_complete**: Receive final report
- **error**: Receive error notifications

## Business Value Proposition

This demo showcases the ability to build sophisticated autonomous agents that can:

- **Automate Research**: Replace hours of manual research with automated intelligence
- **Handle Complex Queries**: Break down and systematically address multi-faceted questions
- **Provide Real-Time Insights**: Show the thinking process, not just final results
- **Scale Knowledge Work**: Handle multiple research tasks simultaneously
- **Integrate Multiple Sources**: Combine information from various web sources
- **Generate Professional Reports**: Produce business-ready documentation

## Use Cases for Client Adaptation

- **Market Research Automation**: Automated competitive analysis and market reports
- **Due Diligence**: Automated research for investment and business decisions
- **Content Creation**: Research-backed article and report generation
- **Business Intelligence**: Automated industry trend analysis
- **Compliance Research**: Regulatory and legal requirement research
- **Academic Research**: Literature review and information synthesis

## Deployment Options

### Development
- Local development with hot reload
- Separate backend and frontend servers

### Production
- Combined Flask application serving React build
- Docker containerization available
- Cloud deployment ready (AWS, GCP, Azure)

## Customization Opportunities

- **Search Sources**: Add Google Search API, academic databases, proprietary sources
- **AI Models**: Integrate different LLMs or specialized models
- **Output Formats**: Generate PDFs, presentations, or structured data
- **Industry Specialization**: Customize for specific domains (finance, healthcare, etc.)
- **Authentication**: Add user management and access control
- **Analytics**: Track usage patterns and research effectiveness

## Security Considerations

- **API Key Management**: Secure storage of OpenAI and search API keys
- **Rate Limiting**: Prevent abuse of search and AI services
- **Content Filtering**: Ensure appropriate content in research results
- **Data Privacy**: Handle sensitive research queries appropriately

## Performance Optimization

- **Caching**: Cache search results and AI responses
- **Parallel Processing**: Concurrent web scraping and analysis
- **Queue Management**: Handle multiple research tasks efficiently
- **Resource Monitoring**: Track API usage and costs

## Future Enhancements

- **Multi-Language Support**: Research in different languages
- **Visual Content**: Include images and charts in reports
- **Citation Management**: Proper source attribution and bibliography
- **Export Options**: PDF, Word, PowerPoint export capabilities
- **Collaboration Features**: Team research and sharing capabilities

## License

This demo is provided for evaluation and demonstration purposes. Commercial use requires appropriate licensing and API access.

## Support

For questions about implementation, customization, or deployment, please contact the development team.

