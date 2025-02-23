import streamlit as st

def handle_text_interaction(model):
    """Handles text-to-text chatbot interaction"""
    user_input = st.text_input('Enter what you want to search')
    button = st.button('Response')

    if button and user_input:
        response = model.generate_content(user_input)
        st.write(response.text)
