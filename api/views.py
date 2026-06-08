import time
import os

from django.shortcuts import render
from django.http import FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils.audio_preprocess import preprocess_audio
from .services.whisper_service import transcribe_audio
from .services.translation_service import TranslationService
from .services.tts_service import synthesize_speech

from .services.english_asr_service import EnglishASRService


# =========================
# UI PAGE
# =========================
def test_page(request):
    return render(request, "test_client.html")


# =========================
# Bangla Speech → English Speech Pipeline
# =========================
@api_view(["POST"])
def speech_to_text(request):

    try:
        total_start = time.time()

        audio = request.FILES.get("audio")

        if not audio:
            return Response({"success": False, "error": "audio missing"}, status=400)

        # PREPROCESS
        preprocess_start = time.time()
        wav_path = preprocess_audio(audio)
        preprocess_time = round(time.time() - preprocess_start, 2)

        # ASR (Bangla)
        asr_start = time.time()
        bangla_text = transcribe_audio(wav_path)
        asr_time = round(time.time() - asr_start, 2)

        # TRANSLATION (BN → EN)
        translation_start = time.time()
        translator = TranslationService()
        english_text = translator.translate(bangla_text)
        translation_time = round(time.time() - translation_start, 2)

        total_time = round(time.time() - total_start, 2)

        return Response({
            "success": True,
            "bangla_text": bangla_text,
            "english_text": english_text,
            "timings": {
                "preprocess_sec": preprocess_time,
                "asr_sec": asr_time,
                "translation_sec": translation_time,
                "total_sec": total_time
            }
        })

    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


# =========================
# TEXT → SPEECH (Piper)
# =========================
@api_view(["POST"])
def text_to_speech(request):

    try:
        text = request.data.get("text")

        if not text:
            return Response({"success": False, "error": "text missing"}, status=400)

        audio_path = synthesize_speech(text)

        return FileResponse(
            open(audio_path, "rb"),
            content_type="audio/wav"
        )

    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)


# =========================
# English Speech → Text (ASR)
# =========================
@api_view(["POST"])
def english_speech_to_text(request):

    try:
        total_start = time.time()

        audio = request.FILES.get("audio")

        if not audio:
            return Response({"success": False, "error": "audio missing"}, status=400)

        # PREPROCESS
        preprocess_start = time.time()
        wav_path = preprocess_audio(audio)
        preprocess_time = round(time.time() - preprocess_start, 2)

        # ENGLISH ASR
        asr_start = time.time()
        english_text = EnglishASRService.transcribe(wav_path)
        asr_time = round(time.time() - asr_start, 2)

        total_time = round(time.time() - total_start, 2)

        return Response({
            "success": True,
            "english_text": english_text,
            "timings": {
                "preprocess_sec": preprocess_time,
                "asr_sec": asr_time,
                "total_sec": total_time
            }
        })

    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)
    

# =========================
# English Text -> Bangla Text
# =========================
@api_view(["POST"])
def translate_en_bn(request):

    try:

        english_text = request.data.get("text", "").strip()

        if not english_text:
            return Response(
                {
                    "success": False,
                    "error": "text missing"
                },
                status=400
            )

        start_time = time.time()

        translator = TranslationService()

        bangla_text = translator.translate_en_to_bn(
            english_text
        )

        total_time = round(
            time.time() - start_time,
            2
        )

        return Response({

            "success": True,

            "english_text": english_text,

            "bangla_text": bangla_text,

            "timings": {
                "translation_sec": total_time,
                "total_sec": total_time
            }

        })

    except Exception as e:

        return Response(
            {
                "success": False,
                "error": str(e)
            },
            status=500
        )