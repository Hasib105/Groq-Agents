import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain import hub
from langchain.agents import AgentExecutor, create_json_chat_agent
from langchain_community.tools.tavily_search import TavilySearchResults

# Load environment variables
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
tavily_key = os.getenv('TAVILY_API_KEY')

# Initialize Groq client
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.1,
    max_tokens=150,
)

st.title("API Query Agent")

# Initialize session state for API URL
if 'api_url' not in st.session_state:
    st.session_state.api_url = None

# Input for API URL
api_url = st.text_input("Enter the API URL:")

if api_url:
    st.session_state.api_url = api_url

# Function to generate a response based on user input using the provided URL
def generate_response(user_input):
    tools = [TavilySearchResults(max_results=1)]
    prompt = hub.pull("hwchase17/react-chat-json")
    
    # Create the agent with the prompt
    agent = create_json_chat_agent(llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
    )
    
    # Combine user input with the provided URL for context
    context = f"Using the API at {st.session_state.api_url}, answer the following question: {user_input}"
    
    # Invoke the agent with the combined context
    response = agent_executor.invoke({"input": context})
    return response["output"]

# Chat input for user messages - only show if an API URL has been provided
if st.session_state.api_url is not None:
    user_input = st.chat_input('Message to Assistant...')
    
    if user_input:
        with st.spinner("Generating response..."):
            # Generate response based on user input and provided URL.
            response = generate_response(user_input)
            
            # Display user's message and assistant's response in a formatted way
            st.markdown("### Your Message:")
            st.markdown(f"> {user_input}")  # Display user's message
            
            st.markdown("### Assistant's Response:")
            st.markdown(f"> {response}")  # Display assistant's response
            
            # Optional: Add a separator for clarity
            st.markdown("---")