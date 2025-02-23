import streamlit as st
import speech_recognition as sr
from tts_engine import speak_text

def handle_voice_interaction(model):
    """Handles voice-to-voice chatbot interaction"""
    st.write("Click the button below and speak to the chatbot.")

    if st.button("🎙️ Start Voice Interaction"):
        recognizer = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                # Adjust for background noise before listening
                recognizer.adjust_for_ambient_noise(source, duration=1)
                st.write("Listening... Speak now!")

                # Listen for the user's speech
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                
                # Convert speech to text
                user_input = recognizer.recognize_google(audio)
                st.write(f"🗣️ You said: {user_input}")

                # Get AI Response
                response = model.generate_content(user_input)
                st.write(f"🤖 AI says: {response.text}")

                # Convert AI response to speech
                speak_text(response.text)

        except sr.WaitTimeoutError:
            st.write("❌ No speech detected within the time limit. Please try again.")
        except sr.UnknownValueError:
            st.write("❌ Sorry, I couldn't understand that. Please speak clearly.")
        except sr.RequestError:
            st.write("❌ There was an issue with the speech recognition service. Please try again.")
