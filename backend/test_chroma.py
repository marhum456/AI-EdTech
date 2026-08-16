import chromadb

from app.config import settings


# =================================================
# Connect to ChromaDB
# =================================================

client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_PATH
)

collection = client.get_or_create_collection(
    name="lesson_embeddings"
)


# =================================================
# Get Metadata Only
# =================================================

results = collection.get(
    include=["metadatas"]
)

metadatas = results["metadatas"]


print("\n==============================================")
print("ChromaDB Metadata")
print("==============================================")

print(f"\nTotal chunks: {len(metadatas)}")


# =================================================
# Display Metadata
# =================================================

for i, metadata in enumerate(metadatas, 1):

    print(f"\nChunk {i}")
    print("-" * 40)

    print(f"Subject      : {metadata.get('subject')}")
    print(f"Course       : {metadata.get('course')}")
    print(f"Lesson       : {metadata.get('lesson')}")
    print(f"Chunk Number : {metadata.get('chunk_number')}")
    print(f"Source       : {metadata.get('source')}")


print("\n==============================================")
print("✅ Metadata inspection completed.")
print("==============================================")