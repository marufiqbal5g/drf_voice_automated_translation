from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services.translation_service import TranslationService
from .utils.audio_preprocess import preprocess_audio
from .services.whisper_service import transcribe_audio

def test_page(request):
    return render(request, 'test_client.html')


@api_view(['POST'])
def speech_to_text(request):

    try:
        audio = request.FILES.get("audio")

        if not audio:
            return Response({
                "error": "audio missing"
            }, status=400)

        # STEP 1: preprocess audio
        wav_path = preprocess_audio(audio)

        # STEP 2: ASR (Bangla text)
        bangla_text = transcribe_audio(wav_path)

        # STEP 3: Translation (English text)
        translator = TranslationService()
        english_text = translator.translate(bangla_text)

        # STEP 4: response
        return Response({
            "success": True,
            "bangla_text": bangla_text,
            "english_text": english_text
        })

    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)