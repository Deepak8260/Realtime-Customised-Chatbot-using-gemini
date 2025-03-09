import gtts
from io import BytesIO

def speak_text(text):
    """Convert text response to speech using gTTS and return audio bytes."""
    try:
        # Convert text to speech
        tts = gtts.gTTS(text, lang="en")

        # Save the audio to a BytesIO object
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)

        # Move cursor to the beginning so Streamlit can read it
        audio_bytes.seek(0)

        return audio_bytes

    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        return None
