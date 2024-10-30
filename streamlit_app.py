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

# Define the Reflection Buddy prompt with instructions for the chatbot
reflection_prompt = """
You are a chatbot that helps students reflect on their learning progress. You guide them through the six phases of the Gibbs Reflection Cycle to promote deep insights and personal growth. If you realize that a phase needs more depth, you should also ask further questions that deepen the user's answers and thoughts. Only go to the next step when you realize that sufficient thought has been given. 

Instructions:
1. Greeting: Start with a friendly and welcoming greeting. Introduce yourself briefly and explain your role.
2. Phase 1 - Description: Ask the student to describe the event or experience with open questions for details.
3. Phase 2 - Feelings: Ask about feelings and thoughts during the experience.
4. Phase 3 - Evaluation: Ask for an assessment of what went well and what could have been better.
5. Phase 4 - Analysis: Help identify reasons for success or failure with deeper questions.
6. Phase 5 - Conclusion: Assist in drawing lessons and insights from the experience.
7. Phase 6 - Action plan: Encourage planning concrete steps for the future with realistic goals.
8. Conclusion: Summarize key points and provide a supportive farewell with further resources if appropriate.
"""

# Initialize the chat messages without displaying the reflection prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": reflection_prompt},  # Only for API, not displayed in the UI
        {"role": "assistant", "content": "Hello! I am your Reflection Buddy. I'm here to guide you through a structured reflection process to help you gain insights and grow from your experiences. Let's start by describing an event or experience you’d like to reflect on. Can you tell me exactly what happened?"}
    ]

# Display the existing chat messages without showing the system prompt
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Create a chat input field for user responses
if user_input := st.chat_input("Your response..."):

    # Store and display the user's input
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate a response from the Reflection Buddy using the OpenAI API with the reflection prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
    )

    # Retrieve the assistant's message content with error handling
    assistant_message = response['choices'][0]['message']['content'] if 'choices' in response and response['choices'] else "I'm sorry, I couldn't generate a response."

    # Display and store the assistant's response in session state
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
