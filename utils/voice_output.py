from gtts import gTTS
import tempfile
import os

def speak(text, lang='hi'):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        tts.save(fp.name)
        os.system(f'start {fp.name}')  # Adjust if you're on Linux or macOS