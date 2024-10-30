import streamlit as st
import openai
import os
import time
import asyncio

# OpenAI API-Key aus Umgebungsvariablen laden
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

# Konfiguriere die Streamlit-Seite
st.set_page_config(page_title="Simple Chatbot", layout="centered")
st.title("💬 Simple Chatbot")
st.write("This chatbot uses OpenAI's GPT model to answer questions.")

# Initialisiere Variablen in der Session State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# Funktion zum Streamen der Antwort
def stream_response(response_text):
    message_placeholder = st.empty()
    full_response = ""
    for char in response_text:
        full_response += char
        message_placeholder.markdown(full_response + "▌")
        time.sleep(0.02)
    message_placeholder.markdown(full_response)
    return full_response

# Chatverlauf anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Eingabe des Benutzers
user_input = st.chat_input("Ask me anything...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Asynchroner API-Aufruf mit der neuen `acreate`-Methode
    async def fetch_response():
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
        )
        return response['choices'][0]['message']['content']

    # Stream die Antwort und füge sie zur Session State hinzu
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        assistant_response = loop.run_until_complete(fetch_response())

        with st.chat_message("assistant"):
            streamed_response = stream_response(assistant_response)

        st.session_state.messages.append({"role": "assistant", "content": streamed_response})
    except Exception as e:
        st.error(f"An error occurred: {e}")
