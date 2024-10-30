import streamlit as st
import openai
from langchain.prompts import ChatPromptTemplate

# Set up page
st.set_page_config(page_title="Reflect Chatbot", layout="centered")
st.title("💬 Rflect Chatbot")
st.write("Hier wird nachher stehen, was wir den Usern als Instruction mitgeben wollen.")

# Load API key from secrets
openai_api_key = st.secrets["openai_api_key"]
openai.api_key = openai_api_key

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Define the ChatPromptTemplate
prompt_template = ChatPromptTemplate.from_template(
    """
    Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context: Chatbot conversation history
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
    """
)

# Get user input and process
user_question = st.chat_input("Your question...")
if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # Format prompt using template
   prompt = ChatPromptTemplate.from_template(
"""
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""
)

parser = StrOutputParser()


    # Call OpenAI API to generate response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )

    # Extract and display response
    assistant_message = response['choices'][0]['message']['content']
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    with st.chat_message("assistant"):
        st.markdown(assistant_message)

st.write("Ask any question above, and the chatbot will respond!")
