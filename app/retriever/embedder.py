from langchain.embeddings import HuggingFaceBgeEmbeddings

def get_embedder():
    return HuggingFaceBgeEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")