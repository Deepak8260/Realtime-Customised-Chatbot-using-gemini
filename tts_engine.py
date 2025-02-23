from gtts import gTTS
import base64
import streamlit as st
import tempfile

def speak_text(text):
    """Convert text to speech using gTTS and automatically play it in Streamlit."""
    try:
        # Generate speech from text
        tts = gTTS(text=text, lang="en")
        
        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            audio_path = temp_audio.name
            tts.save(audio_path)

        # Read the audio file and encode it to base64
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
            b64_audio = base64.b64encode(audio_bytes).decode()

        # Create an HTML audio player with autoplay
        autoplay_audio_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        """

        # Display the audio player in Streamlit
        st.markdown(autoplay_audio_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error generating speech: {e}")
