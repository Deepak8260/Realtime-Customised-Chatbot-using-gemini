import streamlit as st
import speech_recognition as sr
import numpy as np
import tempfile
import scipy.io.wavfile as wav
from tts_engine import speak_text
from streamlit_mic_recorder import mic_recorder

def handle_voice_interaction(model):
    """Handles voice-to-voice chatbot interaction using streamlit-mic-recorder"""
    st.write("Click the button below and speak to the chatbot.")

    # Record audio using streamlit-mic-recorder
    audio_data = mic_recorder(start_prompt="🎤 Click to record and speak...", key="recorder")

    if audio_data:
        try:
            # Save the recorded audio to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name

            # Convert speech to text
            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_audio_path) as source:
                audio = recognizer.record(source)
                user_input = recognizer.recognize_google(audio)
                st.write(f"🗣️ You said: {user_input}")

                # Get AI response
                response = model.generate_content(user_input)
                st.write(f"🤖 AI says: {response.text}")

                # Convert AI response to speech
                speak_text(response.text)

        except sr.UnknownValueError:
            st.write("❌ Could not understand audio. Please try again.")
        except sr.RequestError:
            st.write("❌ Issue with speech recognition service. Please try again.")
