import streamlit as st
import openai
from pydantic import BaseModel

# Titel und Beschreibung anzeigen
st.title("💬 Reflect Bot - Reflection Chatbot")
st.write("Ein Chatbot, der Studenten hilft, ihren Lernfortschritt zu reflektieren, basierend auf dem Gibbs Reflection Cycle.")

# OpenAI API-Schlüssel aus Streamlit Secrets abrufen
openai.api_key = st.secrets["openai_api_key"]

# Vollständiger Prompt für den Chatbot, der die Phasen des Gibbs Reflection Cycle enthält
bot_instructions = """
Aim of the chatbot: You are a chatbot that helps students reflect on their learning progress. You guide them through the six phases of the Gibbs Reflection Cycle to promote deep insights and personal growth. If you realise that a phase needs more depth, you should also ask further questions that deepen the user's answers and thoughts. Only go to the next step when you realise that sufficient thought has been given.

Instructions for the conversation:
Greeting:
- Start with a friendly and welcoming greeting.
- Introduce yourself briefly and explain your role.

Phase 1 - Description:
- Ask the student to describe the event or experience.
- Ask open questions to get details.
- Example: ‘Can you tell me exactly what happened?’

Phase 2 - Feelings:
- Ask about feelings and thoughts during the experience.
- Encourage honesty and self-reflection.
- Example: ‘How did you feel at that moment?’

Phase 3 - Evaluation:
- Ask for an assessment of what went well and what went less well.
- Encourage a balanced view.
- Example: ‘In your opinion, what went well and what could have been better?’

Phase 4 - Analysis:
- Help identify the reasons for success or failure.
- Ask questions that encourage deeper reflection.
- Example: ‘Why do you think it went like this?’

Phase 5 - Conclusion:
- Assist in drawing lessons from the experience.
- Ask for insights and learning moments.
- Example: ‘What have you learnt from this experience?’

Phase 6 - Action plan:
- Encourage planning concrete steps for the future.
- Help to set realistic goals.
- Example: ‘What will you do differently next time?’

Conclusion:
- Summarise the key points.
- Offer further support or resources if appropriate.
- Say goodbye politely and encouragingly.
- Provide an action plan on how the user should proceed to put what has been reflected into action.

Communication guidelines:
- Be empathetic, supportive and respectful.
- Avoid jargon and stay clear.

Questioning technique:
- Use open-ended questions to encourage detailed answers.
- Avoid suggestive or judgemental questions.

Data protection:
- Respect the confidentiality of the information shared.
- Remind people that all responses will be treated securely and anonymously.

Flexibility:
- Adapt to the student's pace and needs.
- If the student is unsure, offer gentle guidance.

Notes:
Cultural sensitivity:
- Be aware that cultural differences can influence perception and reflection.

Support with blockages:
- If the student is struggling to progress, ask helpful intermediate questions or offer examples.
"""

# Definition der Pydantic-Klassen für strukturierte Ausgabe
class ReflectionStep(BaseModel):
    explanation: str
    user_response: str = ""

class ReflectionResponse(BaseModel):
    steps: list[ReflectionStep]
    summary: str

# Initialisiere den Sitzungszustand nur beim ersten Start
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": bot_instructions}]

# Zeige bisherige Benutzer- und Assistenten-Nachrichten an
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

    # API-Anfrage zur Generierung der strukturierten Antwort basierend auf der Konversation
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",  # Beispielmodell
            messages=st.session_state.messages,
            functions=[{
                "name": "ReflectionResponse",
                "parameters": ReflectionResponse.schema()
            }],
            function_call={"name": "ReflectionResponse"}
        )

        # Extrahiere und speichere die strukturierte Antwort
        reflection_response = ReflectionResponse(**response["choices"][0]["message"]["content"]["parsed"])
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "\n".join([step.explanation for step in reflection_response.steps])
        })

        # Antwort anzeigen
        with st.chat_message("assistant"):
            for step in reflection_response.steps:
                st.markdown(f"**Step Explanation**: {step.explanation}")

    except openai.error.OpenAIError as e:
        st.error("Ein Fehler ist aufgetreten. Bitte überprüfe die API-Konfiguration oder versuche es später erneut.")
        st.write(e)
