#!/bin/bash
# Quick start script for chat backend
# Usage: ./START_CHAT_BACKEND.sh

echo "🚀 Starting Todo Chat Backend..."
echo ""

cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please create it first:"
    echo "  cd backend"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate  # or ./venv/Scripts/activate on Windows"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Detect OS and use appropriate Python
if [ -f "venv/Scripts/python.exe" ]; then
    # Windows (WSL or Git Bash)
    PYTHON="./venv/Scripts/python.exe"
    echo "🪟 Detected Windows environment"
elif [ -f "venv/bin/python" ]; then
    # Linux/Mac
    PYTHON="./venv/bin/python"
    echo "🐧 Detected Linux/Mac environment"
else
    echo "❌ Could not find Python in virtual environment"
    exit 1
fi

echo ""
echo "📋 Checking configuration..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Copying from .env.example..."
    cp .env.example .env
    echo "   ✅ Created .env - please update with your API keys"
fi

echo ""
echo "🔥 Starting Uvicorn server..."
echo "   Backend will be available at: http://localhost:8000"
echo "   API docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start the server
$PYTHON -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
