import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from io import StringIO
from langgraph.graph import StateGraph, MessagesState, START, END
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()

if os.getenv('GROQ_API_KEY'):
    api_key = os.getenv('GROQ_API_KEY')
else:
    api_key = st.secrets["GROQ_API_KEY"]


# Initialize Groq client
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.1,
    max_tokens=150,
)

st.title("CSV File Upload and Query")

# Function to generate a response based on user input using the CSV agent
def generate_response(user_input, csv_agent):
    if csv_agent is not None:
        csv_response = csv_agent.invoke({"input": user_input})
        return csv_response["output"]
    else:
        return "CSV agent is not available."

# Initialize session state variables for DataFrame and CSV agent
if 'df' not in st.session_state:
    st.session_state.df = None

if 'csv_agent' not in st.session_state:
    st.session_state.csv_agent = None

# File uploader for CSV files
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the raw content of the uploaded file for debugging purposes
        raw_data = uploaded_file.getvalue().decode("utf-8")
        st.write("Raw data from CSV:", raw_data)  # Debugging line

        # Read the CSV file into a DataFrame and cache it in session state
        st.session_state.df = pd.read_csv(StringIO(raw_data))
        
        if st.session_state.df.empty:
            st.error("The uploaded CSV file is empty.")
        else:
            st.write("Data from CSV:", st.session_state.df)

            # Create a CSV agent using the uploaded file directly with allow_dangerous_code=True
            st.session_state.csv_agent = create_csv_agent(
                llm, 
                uploaded_file, 
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
                verbose=True, 
                allow_dangerous_code=True
            )

            # Generate a summary of the data for input to the API
            csv_data_summary = st.session_state.df.describe().to_string()
            response = generate_response(f"Here is a summary of the uploaded data:\n{csv_data_summary}", st.session_state.csv_agent)
            
            st.write(response)  # Display the response content

    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV file is empty.")
    except pd.errors.ParserError as e:
        st.error(f"Error parsing the CSV file: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Chat input for user messages - only show if a CSV has been uploaded successfully
if st.session_state.csv_agent is not None:
    user_input = st.chat_input('Message to Assistant...')
    
    if user_input:
        with st.spinner("Generating response..."):
            response = generate_response(user_input, st.session_state.csv_agent)
            
            # Display user's message and assistant's response in a formatted way
            st.markdown("### Your Message:")
            st.markdown(f"> {user_input}")  # Display user's message
            
            st.markdown("### Assistant's Response:")
            st.markdown(f"> {response}")  # Display assistant's response
            
            # Optional: Add a separator for clarity
            st.markdown("---")

         