from django.urls import path
from .views import speech_to_text, test_page

urlpatterns = [
    path(
        'speech-to-text/',
        speech_to_text
    ),

    path(
        'test/',
        test_page
    ),

]