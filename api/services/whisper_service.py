from transformers import pipeline

print("Loading Bangla model...")

bn_pipe = pipeline(
    task="automatic-speech-recognition",
    model="Rakib/whisper-tiny-bn",
    device=-1
)

print("Bangla model loaded")


def transcribe_audio(audio_path):
    result = bn_pipe(audio_path)

    print(result)

    return result["text"]