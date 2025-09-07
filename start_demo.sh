#!/bin/bash

# AI Research Agent Demo Startup Script
echo "🤖 Starting AI Research Agent Demo..."
echo "=================================="

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY environment variable not set"
    echo "Please set your OpenAI API key:"
    echo "export OPENAI_API_KEY='your-api-key-here'"
    echo ""
fi

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    else
        return 0
    fi
}

# Check required ports
echo "🔍 Checking ports..."
if ! check_port 5000; then
    echo "Backend port 5000 is busy. Please stop the service or change the port."
    exit 1
fi

if ! check_port 5173; then
    echo "Frontend port 5173 is busy. Please stop the service or change the port."
    exit 1
fi

echo "✅ Ports are available"

# Start backend in background
echo "🚀 Starting backend server..."
cd research-agent-backend
source venv/bin/activate
python src/main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Start frontend in background
echo "🎨 Starting frontend server..."
cd research-agent-frontend
npm run dev --host &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "⏳ Waiting for frontend to initialize..."
sleep 5

echo ""
echo "🎉 Demo is ready!"
echo "=================================="
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend:  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Demo stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Keep script running
wait

