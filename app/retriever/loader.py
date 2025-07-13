import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

DOCS_DIR = "app/docs"

def load_documents():
    all_docs = []

    for filename in os.listdir(DOCS_DIR):
        file_path = os.path.join(DOCS_DIR,filename)

        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif filename.endswith(".txt"):
            loader = TextLoader(file_path)
        else :
            return {"message" : "unsupported file type, please upload .pdf or .txt"}
            continue

        docs = loader.load() 
        for doc in docs:
            doc.metadata["source"] = filename
        all_docs.extend(docs)

    return all_docs




