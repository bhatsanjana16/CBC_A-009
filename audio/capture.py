import asyncio
import pyaudio
import base64
import json

class AudioCapture:
    def __init__(self, ws, rate=16000, chunk=512):
        self.ws = ws
        self.RATE = rate
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.model_speaking = False

    async def capture(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        while True:
            data = await asyncio.to_thread(stream.read, self.CHUNK)
            if not self.model_speaking:
                await self.ws.send(json.dumps({
                    "realtime_input": {
                        "media_chunks": [{
                            "data": base64.b64encode(data).decode(),
                            "mime_type": "audio/pcm",
                        }]
                    }
                }))