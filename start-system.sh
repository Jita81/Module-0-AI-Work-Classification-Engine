#!/bin/bash

# AI Work Classification Engine - Full Stack Startup Script

echo "🚀 Starting AI Work Classification Engine Full Stack System"
echo "============================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r ai-work-classification-engine/requirements.txt"
    exit 1
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Check if Claude API key is set
if [ -z "$CLAUDE_API_KEY" ]; then
    echo "⚠️  Warning: CLAUDE_API_KEY not set. Using demo mode."
    echo "   For full functionality, set: export CLAUDE_API_KEY='your-api-key'"
    export CLAUDE_API_KEY="demo-key"
fi

echo "🔧 Configuration:"
echo "   Backend: http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo "   Claude API Key: ${CLAUDE_API_KEY:0:10}..."

# Start backend in background
echo "🖥️  Starting backend server..."
cd ai-work-classification-engine
source ../venv/bin/activate
python api_server.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check backend health
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend started successfully"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 5

# Check frontend
if curl -s http://localhost:3000/ > /dev/null; then
    echo "✅ Frontend started successfully"
else
    echo "❌ Frontend failed to start"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 AI Work Classification Engine is now running!"
echo "=============================================="
echo "🌐 Open your browser to: http://localhost:3000"
echo ""
echo "📋 Available Features:"
echo "   • Classification Tester - Classify work items with AI"
echo "   • Configuration Manager - Edit classification standards"  
echo "   • Analytics Dashboard - View system performance"
echo "   • Feedback History - Review and learn from feedback"
echo ""
echo "🛑 To stop the system:"
echo "   Press Ctrl+C or run: pkill -f 'api_server.py|vite'"
echo ""

# Keep script running and handle cleanup
trap 'echo "🛑 Stopping services..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT

# Wait for user to stop
wait
