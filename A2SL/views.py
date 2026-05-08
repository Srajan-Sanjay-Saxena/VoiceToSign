import json
import logging
import os
import tempfile

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .nlp_pipeline import process_text
from . import nlp_utils

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Initialise asset registry on first import
# ---------------------------------------------------------------------------
_ASSETS_DIR = os.path.join(settings.BASE_DIR, "assets")
nlp_utils.build_asset_registry(_ASSETS_DIR)


# ---------------------------------------------------------------------------
# Page views
# ---------------------------------------------------------------------------

def home_view(request):
    return render(request, 'home.html')


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    return render(request, 'contact.html')


def animation_view(request):
    if request.method == 'POST':
        text = request.POST.get('sen', '').strip()
        if not text:
            return render(request, 'animation.html', {"error": "Please enter a sentence."})

        try:
            words = process_text(text)
        except Exception as exc:
            logger.exception("NLP pipeline error")
            return render(request, 'animation.html', {"error": f"Processing error: {exc}", "text": text})

        return render(request, 'animation.html', {'words': words, 'text': text})

    return render(request, 'animation.html')


# ---------------------------------------------------------------------------
# API endpoint for Next.js frontend
# ---------------------------------------------------------------------------

@csrf_exempt
def api_animation_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        text = request.POST.get('sen', '').strip()
        if not text:
            return JsonResponse({'error': 'No text provided'}, status=400)

        words = process_text(text)
        return JsonResponse({'words': words, 'text': text})

    except Exception as e:
        logger.exception("API animation error")
        return JsonResponse({'error': str(e)}, status=500)


# ---------------------------------------------------------------------------
# Server-side ASR (faster-whisper)
# ---------------------------------------------------------------------------

_whisper_model = None


def _get_whisper_model():
    """Lazy-load the faster-whisper model (base, CPU)."""
    global _whisper_model
    if _whisper_model is None:
        from faster_whisper import WhisperModel
        _whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
    return _whisper_model


@csrf_exempt
@require_POST
def transcribe_view(request):
    """Accept an audio blob via POST, transcribe with Whisper, return JSON."""
    audio_file = request.FILES.get("audio")
    if not audio_file:
        return JsonResponse({"error": "No audio file provided."}, status=400)

    suffix = ".webm"
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            for chunk in audio_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        model = _get_whisper_model()
        segments, info = model.transcribe(tmp_path, language="en")
        transcript = " ".join(seg.text.strip() for seg in segments)
    except Exception as exc:
        logger.exception("Whisper transcription error")
        return JsonResponse({"error": str(exc)}, status=500)
    finally:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    return JsonResponse({"transcript": transcript})


# ---------------------------------------------------------------------------
# Auth views
# ---------------------------------------------------------------------------

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('animation')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('animation')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect("home")
