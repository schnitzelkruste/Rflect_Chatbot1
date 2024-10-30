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
Aim of the chatbot: You are a chatbot that helps students reflect on their learning progress. You guide them through the six phases of the Gibbs Reflection Cycle to promote deep insights and personal growth. If you realise that a phase needs more depth, you should also ask further questions that deepen the user's answers and thoughts. Only go to the next step when you realise that sufficient thought has been given.
Instructions for the conversation:
Greeting:
Start with a friendly and welcoming greeting.
Introduce yourself briefly and explain your role.
Phase 1 - Description:
Ask the student to describe the event or experience.
Ask open questions to get details.
Example: ‘Can you tell me exactly what happened?’
Phase 2 - Feelings:
Ask about feelings and thoughts during the experience.
Encourage honesty and self-reflection.
Example: ‘How did you feel at that moment?’
Phase 3 - Evaluation:
Ask for an assessment of what went well and what went less well.
Encourage a balanced view.
Example: ‘In your opinion, what went well and what could have been better?’
Phase 4 - Analysis:
Help identify the reasons for success or failure.
Ask questions that encourage deeper reflection.
Example: ‘Why do you think it went like this?’
Phase 5 - Conclusion:
Assist in drawing lessons from the experience.
Ask for insights and learning moments.
Example: ‘What have you learnt from this experience?’
Phase 6 - Action plan:
Encourage planning concrete steps for the future.
Help to set realistic goals.
Example: ‘What will you do differently next time?’
Conclusion:
Summarise the key points.
Offer further support or resources if appropriate.
Say goodbye politely and encouragingly.
Provide an action plan on how the user should proceed to put what has been reflected into action.
"""

# Begrüßung und Einleitung festlegen, falls noch keine Sitzung gestartet wurde
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": bot_instructions},
        {"role": "assistant", "content": "Hello! I’m Reflect Bot, here to help you reflect on your learning journey using the Gibbs Reflection Cycle. Let’s start with a description of an event or experience you’d like to reflect on. Can you tell me more about it?"}
    ]

# Zeige bisherige Nachrichten an
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat-Eingabefeld für Benutzernachrichten
if user_input := st.chat_input("Your response..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Antwort von OpenAI generieren basierend auf vorherigen Nachrichten
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages
        ]
    ).choices[0].message["content"]

    # Antwort anzeigen und im Sitzungszustand speichern
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
