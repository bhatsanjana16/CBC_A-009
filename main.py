# main.py

# from gemini.client import SimpleGeminiVoice
# import asyncio

# if __name__ == "__main__":
#     client = SimpleGeminiVoice()
#     try:
#         asyncio.run(client.start())
#     except KeyboardInterrupt:
#         print("\nUser interrupted. Stopping...")
#         asyncio.run(client.stop_tasks())

from gemini.client import SimpleGeminiVoice
import asyncio

if __name__ == "__main__":
    client = SimpleGeminiVoice()
    try:
        asyncio.run(client.start())
    except KeyboardInterrupt:
        print("\nUser interrupted. Stopping...")
        asyncio.run(client.stop_tasks())
<<<<<<< HEAD



=======
>>>>>>> 6fd9e887dd268d7c1f5d5ca86d04f24ec19f5970
