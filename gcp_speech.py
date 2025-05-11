# from google.cloud import speech
# from google.cloud import texttospeech
# import pyaudio
# import wave
# from playsound import playsound

# def record_audio(filename="input.wav", duration=5):
#     chunk = 1024
#     sample_format = pyaudio.paInt16
#     channels = 1
#     fs = 44100

#     p = pyaudio.PyAudio()
#     stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)
#     frames = []

#     print("Recording... Speak now!")
#     for _ in range(0, int(fs / chunk * duration)):
#         data = stream.read(chunk)
#         frames.append(data)
#     print("Recording stopped.")

#     stream.stop_stream()
#     stream.close()
#     p.terminate()

#     with wave.open(filename, 'wb') as wf:
#         wf.setnchannels(channels)
#         wf.setsampwidth(p.get_sample_size(sample_format))
#         wf.setframerate(fs)
#         wf.writeframes(b''.join(frames))

#     return filename

# def speech_to_text(audio_file):
#     try:
#         client = speech.SpeechClient()
#         with open(audio_file, "rb") as audio:
#             content = audio.read()
#         audio = speech.RecognitionAudio(content=content)
#         config = speech.RecognitionConfig(
#             encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#             sample_rate_hertz=44100,
#             language_code="hi-IN"  # Hindi; change to "ta-IN" for Tamil, "en-IN" for English
#         )
#         response = client.recognize(config=config, audio=audio)
#         return response.results[0].alternatives[0].transcript if response.results else ""
#     except Exception as e:
#         print(f"Speech-to-text error: {e}")
#         return ""

# def text_to_speech(text, output_file="output.wav"):
#     try:
#         client = texttospeech.TextToSpeechClient()
#         synthesis_input = texttospeech.SynthesisInput(text=text)
#         voice = texttospeech.VoiceSelectionParams(
#             language_code="hi-IN", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
#         )
#         audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
#         response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
#         with open(output_file, "wb") as out:
#             out.write(response.audio_content)
#         print(f"Audio saved to {output_file}")
#         playsound(output_file)  # Play the audio
#     except Exception as e:
#         print(f"Text-to-speech error: {e}")

from google.cloud import speech
from google.cloud import texttospeech
import pyaudio
import wave
from playsound import playsound
import json
import asyncio

# Function to record audio from the user
def record_audio(filename="input.wav", duration=5):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)
    frames = []

    print("Recording... Speak now!")
    for _ in range(0, int(fs / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    print("Recording stopped.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))

    return filename

# Function to convert speech (audio) to text using Google Cloud Speech-to-Text API
def speech_to_text(audio_file):
    try:
        client = speech.SpeechClient()
        with open(audio_file, "rb") as audio:
            content = audio.read()
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code="hi-IN"  # Hindi; change to "ta-IN" for Tamil, "en-IN" for English
        )
        response = client.recognize(config=config, audio=audio)
        return response.results[0].alternatives[0].transcript if response.results else ""
    except Exception as e:
        print(f"Speech-to-text error: {e}")
        return ""

# Function to convert text to speech using Google Cloud Text-to-Speech API
def text_to_speech(text, output_file="output.wav"):
    try:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="hi-IN", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        print(f"Audio saved to {output_file}")
        playsound(output_file)  # Play the audio
    except Exception as e:
        print(f"Text-to-speech error: {e}")

# Function to collect user details for eligibility checking
async def collect_user_info(ws):
    speak("To check your eligibility, I need some details.")
    
    # Collect age
    speak("What is your age?")
    age = await collect_input(ws)
    
    # Collect occupation
    speak("What is your occupation?")
    occupation = await collect_input(ws)
    
    # Collect location
    speak("Which state do you live in?")
    location = await collect_input(ws)
    
    return {'age': age, 'occupation': occupation, 'location': location}

# Function to collect user input from speech
async def collect_input(ws):
    response = await ws.recv()
    return response.strip()

# Eligibility check logic (can be customized)
def check_eligibility(user_details):
    # Basic eligibility check: age > 18 and occupation related to farming or small business
    if int(user_details['age']) >= 18 and user_details['occupation'].lower() in ["farmer", "small business owner"]:
        return True
    return False

# Function to handle the user's query
async def handle_query(query, ws):
    # If the user wants to stop or exit
    if query.lower() in ["stop", "exit", "close", "बंद करो"]:
        print("Shutting down.")
        return

    # If the user asks for the eligibility or registration link
    elif "eligibility" in query or "register" in query:
        # Collect user details
        user_details = await collect_user_info(ws)
        
        # Check eligibility
        eligible = check_eligibility(user_details)
        
        if eligible:
            speak("You are eligible! Here's the link for registration.")
            print("Eligible! Sending the registration link...")
            speak("https://gov-scheme-registration-link.com")
        else:
            speak("Sorry, you are not eligible for this scheme.")
            print("Not eligible.")
    
    # If the query is related to market price
    elif "price" in query:
        # Your market price fetching logic
        pass  # Placeholder for market price fetching logic
    
    else:
        print("Fetching from Gemini...")
        await ws.send(json.dumps({"realtime_input": {"text": {"text": query}}}))
