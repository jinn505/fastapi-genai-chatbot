from langchain.memory import ConversationBufferMemory

def get_memory():
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="question",
        output_key="answer"
    )
