from .whisper_service import bn_pipe
from .translation_service import model, tokenizer

def warmup_models():

    print("Warming up models...")

    bn_pipe("dummy.wav")

    tokenizer.encode("আমি ভালো আছি")

    print("Warmup complete ✔")