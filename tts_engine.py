import pyttsx3
import threading

def speak_text(text):
    """Convert text response to speech using a separate thread"""
    def speak():
        tts_engine = pyttsx3.init()
        tts_engine.say(text)
        tts_engine.runAndWait()

    thread = threading.Thread(target=speak)
    thread.start()
