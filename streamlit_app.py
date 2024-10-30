import streamlit as st
import openai

# Titel und Beschreibung anzeigen
st.title("💬 Reflect Bot - Reflection Chatbot")
st.write("Ein Chatbot, der Studenten hilft, ihren Lernfortschritt zu reflektieren, basierend auf dem Gibbs Reflection Cycle.")

# OpenAI API-Schlüssel aus Streamlit Secrets abrufen
openai.api_key = st.secrets["openai_api_key"]

# Vollständiger Prompt für den Chatbot, der die Phasen des Gibbs Reflection Cycle enthält
bot_instructions = """
You are a chatbot that helps students reflect on their learning progress by guiding them through the six phases of the Gibbs Reflection Cycle to promote deep insights and personal growth.
Aim of the chatbot: Guide the user through structured reflection to gain insights and foster personal development.
Instructions:
- Phase 1 (Description): Ask the student to describe the event in detail. E.g., 'Can you tell me exactly what happened?'
- Phase 2 (Feelings): Ask about their feelings during the experience. E.g., 'How did you feel at that moment?'
- Phase 3 (Evaluation): Reflect on what went well and what didn’t. E.g., 'What went well and what could have been improved?'
- Phase 4 (Analysis): Encourage deep analysis. E.g., 'Why do you think it happened this way?'
- Phase 5 (Conclusion): Draw lessons. E.g., 'What have you learned from this experience?'
- Phase 6 (Action Plan): Plan for the future. E.g., 'What will you do differently next time?'
"""

# Initialisiere den Sitzungszustand nur beim ersten Start
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": bot_instructions}]

# Zeige bisherige Benutzer- und Assistenten-Nachrichten an (ohne den system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat-Eingabefeld für Benutzernachrichten
if user_input := st.chat_input("Your response..."):
    # Benutzer-Nachricht hinzufügen
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # API-Anfrage zur Generierung der Antwort basierend auf der Konversation
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Das gewünschte Modell angeben, z.B. "gpt-3.5-turbo" oder "gpt-4"
            messages=st.session_state.messages
        )

        # Extrahiere die Antwort
        assistant_response = response["choices"][0]["message"]["content"]
        
        # Antwort anzeigen und im Sitzungszustand speichern
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

    except openai.error.OpenAIError as e:
        st.error("Ein Fehler ist aufgetreten. Bitte überprüfe die API-Konfiguration oder versuche es später erneut.")
        st.write(e)
