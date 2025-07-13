from qdrant_client import QdrantClient  
from qdrant_client.models import Distance, VectorParams
from langchain_community.vectorstores import Qdrant as QdrantStore
from app.retriever.embedder import get_embedder

def get_qdrant():
    client = QdrantClient(
         url="http://localhost:6333",
        prefer_grpc=False
    )
    embedder = get_embedder()

    if client.collection_exists("chatbot-docs"):
        client.delete_collection("chatbot-docs")

    # dummy_vector = embedder.embed_query("test")
    # vector_dim = len(dummy_vector)

    collection_name = "chatbot-docs"

    # Check and create collection if it doesn't exist
    if not client.collection_exists(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams
            (
                size=len(embedder.embed_query("test")),
                distance=Distance.COSINE),
            )

    # Return wrapped store
    return QdrantStore(
        client=client,
        collection_name=collection_name,
        embeddings=embedder
    )

