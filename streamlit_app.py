import streamlit as st
import openai

# Show title and description.
st.title("💬 Reflection Buddy")
st.write(
    "Reflection Buddy helps students reflect on their learning progress through the Gibbs Reflection Cycle. "
    "This chatbot guides you through each phase to promote deep insights and personal growth."
)

# Retrieve the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["openai_api_key"]

# Set up the OpenAI API key
openai.api_key = openai_api_key

# Initial assistant message
initial_assistant_message = """
Hello! I am your Reflection Buddy. I’m here to help you reflect on your experiences using the Gibbs Reflection Cycle. 
Let's start by describing an event you'd like to reflect on. I’ll guide you through six phases to help you gain insights and set goals for growth.
"""

# Initialize the chat messages without a separate system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": initial_assistant_message}
    ]

# Display the existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field for user responses
if user_input := st.chat_input("Your response..."):

    # Store and display the user's input
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate a response from the Reflection Buddy using the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Set to GPT-4
        messages=st.session_state.messages,
    )

    # Retrieve the assistant's message content with error handling
    assistant_message = response['choices'][0]['message']['content'] if 'choices' in response and response['choices'] else "I'm sorry, I couldn't generate a response."

    # Display and store the assistant's response in session state
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
