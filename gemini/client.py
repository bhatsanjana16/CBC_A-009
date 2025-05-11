import asyncio
import json
from websockets.client import connect
from config import GEMINI_URI, GEMINI_MODEL
from audio.capture import AudioCapture
from audio.playback import AudioPlayback
import base64

class SimpleGeminiVoice:
    def __init__(self):
        self.audio_queue = asyncio.Queue()
        self.model_speaking = False
        self.running = True

    async def start(self):
        self.ws = await connect(GEMINI_URI, extra_headers={"Content-Type": "application/json"})
        await self.ws.send(json.dumps({"setup": {"model": f"models/{GEMINI_MODEL}"}}))
        await self.ws.recv()
        print("Connected to Gemini. Start speaking...")

        self.capture = AudioCapture(self.ws)
        self.playback = AudioPlayback(self.audio_queue)

        await asyncio.gather(
            self.capture.capture(),
            self.stream_audio(),
            self.playback.play()
        )

    async def stream_audio(self):
        async for msg in self.ws:
            response = json.loads(msg)
            try:
                audio_data = response["serverContent"]["modelTurn"]["parts"][0]["inlineData"]["data"]
                if not self.model_speaking:
                    self.model_speaking = True
                self.audio_queue.put_nowait(base64.b64decode(audio_data))
            except KeyError:
                pass

            if response.get("serverContent", {}).get("turnComplete"):
                await asyncio.sleep(0.5)
                self.model_speaking = False
                while not self.audio_queue.empty():
                    self.audio_queue.get_nowait()

    async def stop_tasks(self):
        await self.ws.close()
        self.running = False
        


    
