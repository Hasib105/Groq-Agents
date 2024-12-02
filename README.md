# Groq-Langchain-Agent
This project is a Streamlit application that utilizes the LangChain library to create a chat agent that can be used to generate code based on human instructions. The agent is powered by the Groq API and can be used to generate code in a variety of programming languages.


## Features

* AI Chat Bot for generating response based on human instructions
* CSV Agent for generating response based on a CSV file
* API Agent for generating response based on an API call
* Chart Agent for generating charts based on data in a CSV file
* Search engine Agent with Tavily

## Models
| Model                  | Requests per Minute | Requests per Day | Tokens per Minute | Tokens per Day |
|------------------------|---------------------|------------------|-------------------|----------------|
| llama-3.1-8b-instant   | 30                  | 14,400           | 20,000            | 500,000        |
| mixtral-8x7b-32768     | 30                  | 14,400           | 5,000             | 500,000        |

## Technologies Used

* Streamlit for the web interface
* LangChain for the chat agent
* Groq API for code generation
* Tavily API for search

## Setup

1. Clone the repository
2. Install the required packages with `pipenv install`
3. Create a `.env` file with the following variables:
	* `GROQ_API_KEY=Your GROQ API KEY`
	* `TAVILY_API_KEY=Your TAVILY API KEY`
4. Run the application with `streamlit run app.py`
5. Open a web browser and navigate to `http://localhost:8501`




