import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key = api_key,
    temperature = 0.6,
    max_tokens = 1000
)