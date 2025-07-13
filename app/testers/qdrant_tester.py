from app.retriever.qdrant_wrapper import get_qdrant
from app.retriever.loader import load_documents

qdrant = get_qdrant()
docs = load_documents()

qdrant.add_documents(docs)

results = qdrant.similarity_search("what is the document about", k=1)

print("Top match:")
print(results[0].page_content)

# Sample documents
# docs = [
#     {"page_content": "What is the capital of France?", "metadata": {"source": "wiki"}},
#     {"page_content": "The Eiffel Tower is in Paris.", "metadata": {"source": "wiki"}},
# ]

# # Add to vector store
# qdrant.add_texts([d["page_content"] for d in docs], metadatas=[d["metadata"] for d in docs])

# # Perform a similarity search
# results = qdrant.similarity_search("Where is Eiffel Tower?", k=1)

# print("Top match:")
# print(results[0].page_content)
