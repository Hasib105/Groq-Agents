import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

# Initialize Groq client
client = Groq(api_key=api_key)

def generate_response(user_input):
    try:
        # Create a chat completion request
        chat_completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
            temperature=0.1,
            max_tokens=150,
            top_p=1,
        )

        # Debugging output to inspect the response structure
        print("Chat Completion Response:", chat_completion)

        # Check if response contains choices and return the content of the first choice
        if chat_completion:
            return chat_completion.choices[0].message.content
        else:
            return "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"An error occurred: {str(e)}"

st.title("Groq API Response Streaming")
user_input = st.chat_input('Message to Assistant...')

if user_input:
    with st.spinner("Generating response..."):
        response = generate_response(user_input)
        # Display user's message and assistant's response in a formatted way
        st.markdown("### Your Message:")
        st.markdown(f"> {user_input}")  # Display user's message
            
        st.markdown("### Assistant's Response:")
        st.markdown(f"> {response}")  # Display assistant's response
            
        # Optional: Add a separator for clarity
        st.markdown("---")