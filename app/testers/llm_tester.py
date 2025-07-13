# load_dotenv()

# api_key = os.getenv("GROQ_API_KEY")

# model = ChatGroq(
#     model="llama-3.1-8b-instant",
#     api_key = api_key,
#     temperature = 0.6,
#     max_tokens = 1000
# )

# question = input("ask a question : ")
# response = model.invoke(question)

# print(response.content)
# from app.chains.rag_chain import generate_answer

# question = "Where is the Eiffel Tower?"
# answer = generate_answer(question)
# print(answer)
# app/rag_tester.py

from app.chains.rag_chain import get_rag_chain
from langchain_core.messages import HumanMessage, AIMessage

rag_chain = get_rag_chain()
chat_history = []

# You need to pass only {"question": "..."}, no chat_history
response1 = rag_chain.invoke(
    {"question": "Where is the Eiffel Tower?","chat_history" : chat_history}
)
print("Q1:", response1["answer"])

chat_history.append(HumanMessage(content="Where is the Eiffel Tower?"))
chat_history.append(AIMessage(content=response1["answer"]))

response2 = rag_chain.invoke(
    {"question": "What country is it in?","chat_history" : chat_history}
)
print("Q2:", response2["answer"])

