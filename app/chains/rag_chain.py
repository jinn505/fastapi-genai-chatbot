from langchain.chains import ConversationalRetrievalChain
from app.retriever.qdrant_wrapper import get_qdrant
from app.models.llm_groq import model
from app.chains.memory_chain import get_memory
from langchain_core.prompts import PromptTemplate


def get_rag_chain():
    retriever = get_qdrant().as_retriever()
    memory = get_memory()

    question_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language. Ensure the rephrased question can be understood without the chat history and directly address the subject of the conversation.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
    
    standalone_question_prompt = PromptTemplate.from_template(question_template)

    qa_template = """
You are an intelligent assistant. Use the following context (if any) to answer the question.
If the context is irrelevant or empty, answer the question using your own knowledge.

Context:
{context}

Question:
{question}

Answer:
"""
    qa_prompt = PromptTemplate.from_template(qa_template)

    chain = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        verbose = True,
        condense_question_prompt=standalone_question_prompt,
        combine_docs_chain_kwargs={"prompt": qa_prompt}
    )

    return chain