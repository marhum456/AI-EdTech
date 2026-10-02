import chromadb

from app.config import settings

client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_PATH
)

collection = client.get_collection(
    name="lesson_embeddings"
)

results = collection.get(
    where={
        "$and": [
            {"subject": "physics"},
            {"course": "work"},
            {"lesson": "lesson_1"}
        ]
    },
    include=["metadatas"]
)

ids = results["ids"]

print(f"Found {len(ids)} Chemistry chunks.")

if ids:
    collection.delete(ids=ids)
    print(f"Deleted {len(ids)} Chemistry chunks.")

remaining = collection.get(
    where={
        "$and": [
            {"subject": "physics"},
            {"course": "work"},
            {"lesson": "lesson_1"}
        ]
    }
)

print(f"Remaining chunks: {len(remaining['ids'])}")