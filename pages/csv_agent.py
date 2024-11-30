import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from io import StringIO

# Load environment variables
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

# Initialize Groq client
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.1,
    max_tokens=150,
)

st.title("Media File Upload and Query")

# Function to generate a response based on user input using the CSV agent
def generate_response(user_input, csv_agent):
    if csv_agent is not None:
        # Use the CSV agent to process user input related to CSV data
        csv_response = csv_agent.invoke({"input": user_input})
        return csv_response
    else:
        return "CSV agent is not available."

# Specify the directory for storing media files
media_directory = "media"  # Change this to your actual media directory path

# Check if the media directory exists, create if it doesn't
if not os.path.exists(media_directory):
    os.makedirs(media_directory)

# File uploader for CSV files
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Initialize csv_agent variable
csv_agent = None

if uploaded_file is not None:
    try:
        # Read the raw content of the uploaded file for debugging purposes
        raw_data = uploaded_file.getvalue().decode("utf-8")
        st.write("Raw data from CSV:", raw_data)  # Debugging line

        # Read the CSV file into a DataFrame
        df = pd.read_csv(StringIO(raw_data))
        
        if df.empty:
            st.error("The uploaded CSV file is empty.")
        else:
            st.write("Data from CSV:", df)

            # Save the uploaded file to the media directory
            file_path = os.path.join(media_directory, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Create a CSV agent using the uploaded file directly with allow_dangerous_code=True
            csv_agent = create_csv_agent(llm, uploaded_file, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, allow_dangerous_code=True)

            # Generate a summary of the data for input to the API
            csv_data_summary = df.describe().to_string()
            response = generate_response(f"Here is a summary of the uploaded data:\n{csv_data_summary}", csv_agent)
            
            st.write(response)  # Display the response content

    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV file is empty.")
    except pd.errors.ParserError as e:
        st.error(f"Error parsing the CSV file: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Chat input for user messages
user_input = st.chat_input('Message to Assistant...')

if user_input:
    with st.spinner("Generating response..."):
        response = generate_response(user_input, csv_agent)
        st.write(response)  # Display the response content
        
        st.markdown("**Message:** " + user_input)
        st.markdown("---")

# Optionally, display existing files in the media directory for selection or reference
if os.listdir(media_directory):
    st.subheader("Existing Media Files:")
    for filename in os.listdir(media_directory):
        st.write(filename)