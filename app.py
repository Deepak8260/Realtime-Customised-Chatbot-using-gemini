import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from text_interaction import handle_text_interaction
from voice_interaction import handle_voice_interaction

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GENAI_API_KEY")

if not api_key:
    st.error("API Key is missing! Please set GENAI_API_KEY in your .env file.")
else:
    # Configure API key
    genai.configure(api_key=api_key)

    # Load the model
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Streamlit UI
    st.title('Realtime Chatbot App')

    # User selects interaction mode
    mode = st.radio("Select Interaction Mode:", ["Text-to-Text", "Voice-to-Voice"])

    if mode == "Text-to-Text":
        handle_text_interaction(model)  # Call text interaction function

    elif mode == "Voice-to-Voice":
        handle_voice_interaction(model)  # Call voice interaction function