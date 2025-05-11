import pyaudio
import asyncio

class AudioPlayback:
    def __init__(self, audio_queue):
        self.audio_queue = audio_queue
        self.RATE = 24000
        self.CHANNELS = 1
        self.FORMAT = pyaudio.paInt16

    async def play(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, output=True)
        while True:
            data = await self.audio_queue.get()
            await asyncio.to_thread(stream.write, data)

# import simpleaudio as sa
# import asyncio

# class AudioPlayback:
#     def __init__(self, audio_queue):
#         self.audio_queue = audio_queue
#         self.running = True

#     async def play(self):
#         try:
#             while self.running:
#                 data = await self.audio_queue.get()
#                 wave_obj = sa.WaveObject(data, num_channels=1, bytes_per_sample=2, sample_rate=24000)
#                 play_obj = wave_obj.play()
#                 await asyncio.to_thread(play_obj.wait_done)
#         except asyncio.CancelledError:
#             print("Playback cancelled.")

