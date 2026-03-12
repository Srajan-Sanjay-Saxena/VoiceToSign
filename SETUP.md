# Voice2Sign - Next.js + Django Setup Guide

## Complete Setup Instructions

### 1. Django Backend Setup

```bash
# Navigate to project root
cd "/Users/srajansaxena/Desktop/Ug stuff/Voice2sign-main"

# Create virtual environment (if not exists)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies including CORS
pip install -r requirements.txt

# Run Django server
python manage.py runserver
```

Django will run on: `http://localhost:8000`

### 2. Next.js Frontend Setup

```bash
# Navigate to Next.js app
cd voice_to_isl

# Install dependencies
pnpm install

# Run development server
pnpm dev
```

Next.js will run on: `http://localhost:3000`

### 3. Access the Application

Open your browser and go to: `http://localhost:3000`

## Important Notes

- **Django backend must be running** on port 8000 for the frontend to work
- **Chrome browser recommended** for speech recognition features
- CORS is configured to allow requests from localhost:3000
- All video assets are served from Django's static files

## Features

✅ Modern Next.js UI with TypeScript
✅ Real-time speech recognition
✅ Django backend for text processing
✅ 3D ISL animation playback
✅ Responsive design with Tailwind CSS
✅ Glassmorphism UI effects

## Troubleshooting

**If videos don't load:**
- Ensure Django server is running
- Check that assets folder contains .mp4 files
- Verify CORS settings in Django

**If speech recognition doesn't work:**
- Use Chrome browser
- Allow microphone permissions
- Check browser console for errors
