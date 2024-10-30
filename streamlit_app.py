import streamlit as st
from openai import OpenAI
from pydantic import BaseModel

# Titel und Beschreibung anzeigen
st.title("💬 Reflect Bot - Reflection Chatbot")
st.write("Ein Chatbot, der Studenten hilft, ihren Lernfortschritt zu reflektieren, basierend auf dem Gibbs Reflection Cycle.")

# OpenAI API-Schlüssel aus Streamlit Secrets abrufen
openai_api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=openai_api_key)

# Prompt-Text für den Chatbot definieren, basierend auf dem Gibbs Reflection Cycle
bot_instructions = """
You are a chatbot that helps students reflect on their learning progress. You guide them through the six phases of the Gibbs Reflection Cycle to promote deep insights and personal growth. 
...

"""

# Initialisiere den Sitzungszustand nur beim ersten Start
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": bot_instructions}]

# Zeige bisherige Benutzer- und Assistenten-Nachrichten an (ohne den system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":  # System prompt nicht anzeigen
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat-Eingabefeld für Benutzernachrichten
if user_input := st.chat_input("Your response..."):
    # Benutzer-Nachricht hinzufügen
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Antwort von OpenAI generieren basierend auf vorherigen Nachrichten
    try:
        response = client.chat_completions.create(
            model="gpt-3.5-turbo",  # Oder das spezifische GPT-4 Modell
            messages=st.session_state.messages
        ).choices[0].message["content"]

        # Antwort anzeigen und im Sitzungszustand speichern
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

    except Exception as e:
        st.error("Ein Fehler ist aufgetreten. Bitte überprüfe die API-Konfiguration oder versuche es später erneut.")
        st.write(e)
