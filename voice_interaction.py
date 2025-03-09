import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import numpy as np
from gtts import gTTS
import os

def record_audio(duration=5, sample_rate=16000):
    """Record audio from the microphone and return it as a NumPy array."""
    st.write("🎤 Listening... Speak now.")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()  # Wait for recording to complete
    return np.squeeze(audio_data)

def handle_voice_interaction(model):
    """Handles voice-based interaction with the chatbot model."""
    st.write("Click the button below to start recording your voice.")
    
    # ✅ Button to trigger voice recording
    if st.button("🎙️ Start Recording"):
        recognizer = sr.Recognizer()
        
        # Record voice
        audio_array = record_audio()
        audio_data = sr.AudioData(audio_array.tobytes(), sample_rate=16000, sample_width=2)
        
        try:
            text = recognizer.recognize_google(audio_data)
            st.write(f"🗣️ You said: {text}")

            # ✅ Generate response using Gemini model
            response = model.generate_content(text)
            response_text = response.text  # Extract the generated text

            st.write(f"🤖 Bot: {response_text}")

            # Convert response text to speech
            tts = gTTS(response_text, lang="en")
            tts.save("response.mp3")
            os.system("start response.mp3")  # Windows: 'start', Linux: 'mpg321', Mac: 'afplay'

        except sr.UnknownValueError:
            st.write("❌ Sorry, could not understand the audio.")
        except sr.RequestError:
            st.write("❌ Could not request results, check your internet connection.")
