import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav
from tts_engine import speak_text

def record_audio(duration=5, samplerate=44100):
    """Record audio using sounddevice instead of PyAudio."""
    st.write("🎤 Listening... Speak now!")
    try:
        # Record audio from microphone
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
        sd.wait()  # Wait for the recording to complete

        # Save as a WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            wav.write(temp_audio.name, samplerate, audio_data)
            return temp_audio.name
    except Exception as e:
        st.error(f"⚠️ Error recording audio: {e}")
        return None

def handle_voice_interaction(model):
    """Handles voice-to-voice chatbot interaction"""
    st.write("Click the button below and speak to the chatbot.")

    if st.button("🎙️ Start Voice Interaction"):
        recognizer = sr.Recognizer()
        
        # Record audio input
        audio_file = record_audio(duration=5)

        if audio_file:
            try:
                with sr.AudioFile(audio_file) as source:
                    audio = recognizer.record(source)  # Convert to recognizer format
                    user_input = recognizer.recognize_google(audio)  # Speech-to-Text
                    st.write(f"🗣️ You said: {user_input}")

                    # Get AI Response
                    response = model.generate_content(user_input)
                    st.write(f"🤖 AI says: {response.text}")

                    # Convert AI response to speech
                    speak_text(response.text)

            except sr.UnknownValueError:
                st.write("❌ Could not understand audio. Please try again.")
            except sr.RequestError:
                st.write("❌ Issue with speech recognition service. Please try again.")
