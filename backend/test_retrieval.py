from app.services.embedding_service import embedding_service
from app.services.vector_service import vector_service

query = "Explain JavaScript variables."

query_embedding = embedding_service.embed_text(query)

results = vector_service.search(
    query_embedding,
    n_results=3,
    where={
        "$and": [
            {"subject": "javascript"},
            {"lesson": "lesson_1"}
        ]
    }
)

print("\nRetrieved Chunks:\n")

for i, doc in enumerate(results["documents"][0], start=1):
    print("=" * 60)
    print(f"Chunk {i}")
    print("=" * 60)
    print(doc)
    print()