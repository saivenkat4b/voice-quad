"""
from dotenv import load_dotenv
load_dotenv()  # Loading all the environment variables
"""

import streamlit as st
#import os
import google.generativeai as genai
import pyttsx3

# Configure the generative AI model
api_key = "AIzaSyBkeZC0VC4VdcPexBMro5nqpDwFQAw-3EU"  #GOOGLE_API_KEY
if not api_key:
    st.error("API key not found. Please set the GOOGLE_API_KEY in the .env file.")
else:
    genai.configure(api_key=api_key)

    # Function to load Gemini Pro model and get responses
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])

    def get_gemini_response(question):
        try:
            response = chat.send_message(question, stream=True)
            return response
        except Exception as e:
            st.error(f"Error getting response from Gemini Pro model: {e}")
            return []

    # Initialize our Streamlit app
    st.set_page_config(page_title="Team Quadrant")
    st.header("Quadrant Bot")

    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    input_text = st.text_input("Input: ", key="input")
    submit = st.button("Generate response")

    if submit and input_text:
        response = get_gemini_response(input_text)
        st.session_state['chat_history'].append(("You", input_text))
        st.subheader("The Response is")

        full_response = ""
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))
            full_response += chunk.text + " "

        if full_response:
            # Initialize the text-to-speech engine
            engine = pyttsx3.init()

            # Set properties (optional)
            engine.setProperty('rate', 150)  # Speed percent (can go over 100)
            engine.setProperty('volume', 1)  # Volume 0-1

            # Speak the generated response
            engine.say(full_response)
            engine.runAndWait()

    st.subheader("The Chat History is")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
