import subprocess
import uuid
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PIPER_PATH = r"C:\piper\piper.exe"
MODEL_PATH = r"C:\piper\models\en_US-lessac-medium.onnx"

OUTPUT_DIR = os.path.join(BASE_DIR, "media", "tts")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def synthesize_speech(text: str) -> str:
    """
    English text → WAV audio using Piper TTS
    returns file path
    """

    if not text:
        raise ValueError("Empty text for TTS")

    file_name = f"tts_{uuid.uuid4().hex}.wav"
    output_path = os.path.join(OUTPUT_DIR, file_name)

    cmd = [
        PIPER_PATH,
        "--model",
        MODEL_PATH,
        "--output_file",
        output_path
    ]

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        text=True
    )

    process.communicate(input=text)

    if process.returncode != 0:
        raise Exception("Piper TTS failed")

    return output_path