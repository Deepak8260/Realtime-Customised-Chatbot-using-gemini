import streamlit as st
import speech_recognition as sr
import numpy as np
import tempfile
import wave
from tts_engine import speak_text
from streamlit_mic_recorder import mic_recorder

def handle_voice_interaction(model):
    """Handles voice-to-voice chatbot interaction using streamlit-mic-recorder"""
    st.write("Click the button below and speak to the chatbot.")

    # Record audio using streamlit-mic-recorder
    audio_data = mic_recorder(start_prompt="🎤 Click to record and speak...", key="recorder")

    if audio_data and "bytes" in audio_data:  # ✅ Ensure bytes exist
        try:
            # Save the recorded audio as a valid WAV file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                with wave.open(temp_audio, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Mono channel
                    wav_file.setsampwidth(2)  # Sample width of 2 bytes
                    wav_file.setframerate(44100)  # Standard sample rate
                    wav_file.writeframes(audio_data["bytes"])  # ✅ Write proper WAV format
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
