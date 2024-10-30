import streamlit as st
import openai
from langchain.prompts import ChatPromptTemplate

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you don't need to provide an OpenAI API key."
)

# Retrieve the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["openai_api_key"]

# Set up the OpenAI API key
openai.api_key = openai_api_key

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Define the ChatPromptTemplate
prompt_template = ChatPromptTemplate.from_template(
    """
    Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
    """
)

# Create a chat input field to allow the user to enter a message.
if user_input := st.chat_input("What is up?"):

    # Store and display the user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate a prompt with context and question
    prompt = prompt_template.format(context="Chatbot conversation history.", question=user_input)

    # Call the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract and display the assistant's response
    assistant_message = response['choices'][0]['message']['content']
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
