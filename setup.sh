#!/bin/bash

# AI Work Classification Engine Setup Script

echo "🚀 Setting up AI Work Classification Engine"
echo "=========================================="

# Check if Claude API key is provided
if [ -z "$1" ]; then
    echo "❌ Please provide your Claude API key as an argument:"
    echo "   ./setup.sh YOUR_CLAUDE_API_KEY"
    echo ""
    echo "💡 Get your Claude API key from: https://console.anthropic.com/"
    exit 1
fi

CLAUDE_API_KEY="$1"

echo "🔑 Setting up Claude API key..."
export CLAUDE_API_KEY="$CLAUDE_API_KEY"

# Add to shell profile for persistence
if [ -f ~/.zshrc ]; then
    echo "export CLAUDE_API_KEY='$CLAUDE_API_KEY'" >> ~/.zshrc
    echo "✅ Added to ~/.zshrc"
elif [ -f ~/.bashrc ]; then
    echo "export CLAUDE_API_KEY='$CLAUDE_API_KEY'" >> ~/.bashrc
    echo "✅ Added to ~/.bashrc"
elif [ -f ~/.bash_profile ]; then
    echo "export CLAUDE_API_KEY='$CLAUDE_API_KEY'" >> ~/.bash_profile
    echo "✅ Added to ~/.bash_profile"
fi

echo "🐍 Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r ai-work-classification-engine/requirements.txt

echo "📦 Setting up frontend dependencies..."
cd frontend
npm install
cd ..

echo "🧪 Running tests..."
cd ai-work-classification-engine
source ../venv/bin/activate
python -m pytest tests/test_classification.py --disable-warnings -q
cd ..

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo "🌐 To start the system:"
echo "   ./start-system.sh"
echo ""
echo "🌐 Then open: http://localhost:3000"
echo ""
echo "📋 Available Features:"
echo "   • AI-powered work classification"
echo "   • Real-time feedback and learning"
echo "   • Configuration management"
echo "   • Analytics and reporting"
