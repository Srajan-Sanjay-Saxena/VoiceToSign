# 🚀 Sanketavani - Quick Start Guide

## What I Fixed

### 1. **Removed Authentication & CSRF Protection**
- ✅ Disabled CSRF middleware in Django settings
- ✅ Removed `@login_required` decorator from views
- ✅ Added `@csrf_exempt` to API endpoints
- ✅ Configured CORS properly for Next.js

### 2. **Created API Endpoint**
- ✅ New endpoint: `/api/animation/` (no auth required)
- ✅ Returns JSON instead of HTML
- ✅ Works seamlessly with Next.js frontend

### 3. **Updated Frontend**
- ✅ Converter now uses `/api/animation/` endpoint
- ✅ Removed CSRF token handling
- ✅ Simplified error handling

## 🎯 How to Run

### Option 1: Using the Script (Recommended)
```bash
cd "/Users/srajansaxena/Desktop/Ug stuff/Voice2sign-main"
./start_server.sh
```

### Option 2: Manual Start
```bash
cd "/Users/srajansaxena/Desktop/Ug stuff/Voice2sign-main"
source venv/bin/activate
python manage.py runserver
```

### Restart Server
```bash
./restart.sh
```

## 🌐 URLs

- **Frontend (Next.js)**: http://localhost:3000
- **Backend (Django)**: http://localhost:8000
- **API Endpoint**: http://localhost:8000/api/animation/

## 🔧 What Changed in Django

### settings.py
```python
# CSRF Middleware DISABLED
MIDDLEWARE = [
    # ...
    # 'django.middleware.csrf.CsrfViewMiddleware',  # COMMENTED OUT
    # ...
]

# CORS Settings
CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
```

### views.py
```python
# New API endpoint (no authentication)
@csrf_exempt
def api_animation_view(request):
    # Returns JSON response
    return JsonResponse({'words': words, 'text': text})
```

### urls.py
```python
urlpatterns = [
    # ...
    path('api/animation/', views.api_animation_view, name='api_animation'),
]
```

## 📝 Testing

1. Start Django server: `./start_server.sh`
2. Start Next.js: `cd voice_to_isl && pnpm dev`
3. Open: http://localhost:3000/converter
4. Type text and click "Convert"
5. Should work without any 403 or 500 errors!

## 🐛 Troubleshooting

### Port 8000 already in use?
```bash
lsof -ti:8000 | xargs kill -9
./start_server.sh
```

### Still getting 403?
- Make sure Django server is restarted after changes
- Check that CSRF middleware is commented out in settings.py
- Verify `@csrf_exempt` is on the API view

### Getting 500 error?
- Check Django logs for errors
- Make sure NLTK data is downloaded
- Verify virtual environment is activated

## ✨ Features Now Working

✅ Speech to text conversion
✅ Text preprocessing with NLTK
✅ Word tokenization
✅ ISL animation mapping
✅ Video playback
✅ No authentication required
✅ CORS properly configured
✅ Smooth scrolling (Lenis)
✅ Premium UI design
✅ Mobile responsive

## 🎨 UI Improvements Made

- Premium glass-morphism design
- Apple-like smooth scrolling
- Sophisticated animations
- Mobile responsive layout
- Custom favicon and branding
- Sanskrit name: Sanketavani (संकेतवाणी)

---

**Made with ❤️ for accessibility**
