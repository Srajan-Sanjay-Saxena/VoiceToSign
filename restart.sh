#!/bin/bash

echo "🔄 Restarting Sanketavani Django Server..."

# Kill existing server
pkill -f "python.*manage.py runserver"
sleep 1

# Navigate to project directory
cd "$(dirname "$0")"

# Start server
source venv/bin/activate
python manage.py runserver

echo "✅ Server restarted!"
