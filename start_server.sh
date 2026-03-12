#!/bin/bash

# Sanketavani Django Server Restart Script
# This script kills any process using port 8000 and starts the Django server

echo "🔍 Checking for processes on port 8000..."

# Find and kill any process using port 8000
PORT=8000
PID=$(lsof -ti:$PORT)

if [ ! -z "$PID" ]; then
    echo "⚠️  Found process $PID using port $PORT"
    echo "🔪 Killing process..."
    kill -9 $PID
    sleep 1
    echo "✅ Process killed successfully"
else
    echo "✅ Port $PORT is free"
fi

# Navigate to project directory
cd "$(dirname "$0")"

echo ""
echo "🚀 Starting Sanketavani Django Server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Activate virtual environment and start server
source venv/bin/activate

echo "📦 Virtual environment activated"
echo "🌐 Starting server on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run Django server
python manage.py runserver
