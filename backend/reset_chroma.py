import chromadb

from app.config import settings

client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_PATH
)

client.delete_collection(
    name="lesson_embeddings"
)

print("✅ Old ChromaDB collection deleted.")