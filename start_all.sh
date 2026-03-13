#!/bin/bash

# Sanketavani - Start All Servers
# This script starts both Django backend and Next.js frontend

echo "🎙️ Starting Sanketavani (संकेतवाणी)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Kill any existing processes on ports 8000 and 3000
echo "🔍 Checking for existing processes..."

# Kill Django server (port 8000)
PORT_8000=$(lsof -ti:8000)
if [ ! -z "$PORT_8000" ]; then
    echo "⚠️  Killing Django server on port 8000..."
    kill -9 $PORT_8000
    sleep 1
fi

# Kill Next.js server (port 3000)
PORT_3000=$(lsof -ti:3000)
if [ ! -z "$PORT_3000" ]; then
    echo "⚠️  Killing Next.js server on port 3000..."
    kill -9 $PORT_3000
    sleep 1
fi

echo "✅ Ports cleared"
echo ""

# Start Django server in background
echo "🐍 Starting Django Backend Server..."
cd "$SCRIPT_DIR"
source venv/bin/activate
python manage.py runserver > django.log 2>&1 &
DJANGO_PID=$!
echo "✅ Django server started (PID: $DJANGO_PID)"
echo "   URL: http://localhost:8000"
echo ""

# Wait a moment for Django to start
sleep 2

# Start Next.js server in background
echo "⚛️  Starting Next.js Frontend Server..."
cd "$SCRIPT_DIR/voice_to_isl"
source ~/.nvm/nvm.sh
nvm use node > /dev/null 2>&1
pnpm dev > nextjs.log 2>&1 &
NEXTJS_PID=$!
echo "✅ Next.js server started (PID: $NEXTJS_PID)"
echo "   URL: http://localhost:3000"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Sanketavani is now running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo ""
echo "📝 Logs:"
echo "   Django:  $SCRIPT_DIR/django.log"
echo "   Next.js: $SCRIPT_DIR/voice_to_isl/nextjs.log"
echo ""
echo "To stop servers, run: ./stop_servers.sh"
echo "Or press Ctrl+C and run: pkill -f 'python.*manage.py' && pkill -f 'node.*next'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Save PIDs to file for easy stopping
echo "$DJANGO_PID" > "$SCRIPT_DIR/.django.pid"
echo "$NEXTJS_PID" > "$SCRIPT_DIR/.nextjs.pid"

# Keep script running
wait
