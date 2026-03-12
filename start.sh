#!/bin/bash

# Sanketavani Startup Script
echo "🚀 Starting Sanketavani (संकेतवाणी)..."
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Start Django backend
echo "📡 Starting Django Backend Server..."
cd "$SCRIPT_DIR"
source venv/bin/activate
python manage.py runserver &
DJANGO_PID=$!
echo "✅ Django server started on http://localhost:8000 (PID: $DJANGO_PID)"
echo ""

# Wait a bit for Django to start
sleep 3

# Start Next.js frontend
echo "⚛️  Starting Next.js Frontend..."
cd "$SCRIPT_DIR/voice_to_isl"
source ~/.nvm/nvm.sh
nvm use node
pnpm dev &
NEXTJS_PID=$!
echo "✅ Next.js server started on http://localhost:3000 (PID: $NEXTJS_PID)"
echo ""

echo "🎉 Sanketavani is running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $DJANGO_PID $NEXTJS_PID; exit" INT
wait
