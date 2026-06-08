import uuid
import os
from gtts import gTTS

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

OUTPUT_DIR = os.path.join(BASE_DIR, "media", "bangla_tts")
os.makedirs(OUTPUT_DIR, exist_ok=True)


class BanglaTTSService:

    @staticmethod
    def synthesize(text: str) -> str:

        if not text:
            raise ValueError("Empty text for Bangla TTS")

        file_name = f"bn_tts_{uuid.uuid4().hex}.mp3"
        output_path = os.path.join(OUTPUT_DIR, file_name)

        try:
            tts = gTTS(
                text=text,
                lang="bn",
                slow=False
            )

            tts.save(output_path)

            return output_path

        except Exception as e:
            print("[BANGLA TTS ERROR]", repr(e))
            raise