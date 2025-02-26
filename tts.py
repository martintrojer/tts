import subprocess
import sys
from tempfile import NamedTemporaryFile

import numpy as np
import soundfile as sf
from kokoro import KPipeline


def generate_audio(text: str, voice="af_heart", speed=1.25):
    # 🇺🇸 'a' => American English, 🇬🇧 'b' => British English
    pipeline = KPipeline(
        lang_code="a", device="mps"
    )  # <= make sure lang_code matches voice

    generator = pipeline(text, voice=voice, speed=speed)
    for gs, ps, audio in generator:
        yield audio


def main():
    text = sys.stdin.read().strip()
    all_audio = np.array([])
    for audio in generate_audio(text):
        all_audio = np.append(all_audio, audio)
    with NamedTemporaryFile(suffix=".wav", delete=True) as tmpfile:
        sf.write(tmpfile.name, all_audio, 24000)
        print(f"Playing audio {tmpfile.name}")
        subprocess.run(
            ["vlc", "--play-and-exit", tmpfile.name],
        )


if __name__ == "__main__":
    main()
