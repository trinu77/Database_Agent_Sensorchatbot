import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent 

# Load Gemini API key
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

# Connect to MySQL database
db = SQLDatabase.from_uri(
    "mysql+mysqlconnector://root:trina@localhost:3306/sensor_db"
)

# Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=gemini_key, temperature=0)

# Toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# SQL Agent
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

def run_cmd_chatbot():
    print("🤖 CMD SQL Chatbot connected to sensor_db (type 'exit' to quit)")
    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break

        try:
            response = agent_executor.run(query)
            print(f"Bot: {response}")
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    run_cmd_chatbot()
