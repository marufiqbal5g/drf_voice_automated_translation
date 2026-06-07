from django.urls import path
from .views import speech_to_text, text_to_speech, test_page

urlpatterns = [
    path('speech-to-text/', speech_to_text),
    path('text-to-speech/', text_to_speech),   # NEW
    path('test/', test_page),
]