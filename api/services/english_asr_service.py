from faster_whisper import WhisperModel


print("Loading English Faster-Whisper model...")


class EnglishASRService:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            cls._model = WhisperModel(
                "tiny.en",
                device="cpu",
                compute_type="int8"
            )

            print("English Faster-Whisper loaded")

        return cls._model

    @classmethod
    def transcribe(cls, audio_path):

        model = cls.get_model()

        segments, info = model.transcribe(
            audio_path,
            language="en",
            beam_size=1
        )

        text = " ".join(
            segment.text
            for segment in segments
        )

        return text.strip()