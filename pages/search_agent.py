import os
import streamlit as st
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
if 'TAVILY_API_KEY' in os.environ:
    tavily_key = os.getenv('TAVILY_API_KEY')
else:
    tavily_key = st.secrets["TAVILY_API_KEY"]

# Initialize Tavily Search API
tavily_search = TavilySearchResults(max_results=5)

def tavily_search_query(query):
    """Function to perform a search using the Tavily API."""
    return tavily_search.invoke({"query": query})

# Streamlit app interface
st.title("Tavily Search Engine")

user_input = st.text_input("Enter your search query:")

if user_input:
    with st.spinner("Searching..."):
        # Perform Tavily Search
        tavily_results = tavily_search_query(user_input)
        
        st.markdown("### Tavily Search Results:")
        if tavily_results:
            for index, result in enumerate(tavily_results):
                url = result.get('url', '#')
                content = result.get('content', 'No Content Available')
                st.markdown(f"{index + 1}. {content} [Source]({url})")
        else:
            st.markdown("No results found.")
