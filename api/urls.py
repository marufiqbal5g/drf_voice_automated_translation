from django.urls import path
from .views import (
    speech_to_text,
    text_to_speech,
    english_speech_to_text,
    translate_en_bn,
    bangla_text_to_speech,
    test_page
)

urlpatterns = [
    path('speech-to-text/', speech_to_text),
    path('text-to-speech/', text_to_speech),
    path('english-speech-to-text/', english_speech_to_text),
    path('translate-en-bn/', translate_en_bn),

    # NEW
    path('bangla-text-to-speech/', bangla_text_to_speech),

    path('test/', test_page),
]