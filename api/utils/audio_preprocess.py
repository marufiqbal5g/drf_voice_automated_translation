from pydub import AudioSegment
import tempfile
import os


def preprocess_audio(uploaded_file):

    input_fd, input_path = tempfile.mkstemp(
        suffix=".webm"
    )

    os.close(input_fd)

    with open(
        input_path,
        "wb"
    ) as f:

        for chunk in uploaded_file.chunks():

            f.write(chunk)

    audio = AudioSegment.from_file(
        input_path,
        format="webm"
    )

    audio = audio.set_frame_rate(
        16000
    )

    audio = audio.set_channels(
        1
    )

    audio = audio.normalize()

    output_path = input_path.replace(
        ".webm",
        ".wav"
    )

    audio.export(
        output_path,
        format="wav"
    )

    os.remove(
        input_path
    )

    return output_path