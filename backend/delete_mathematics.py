import chromadb

from app.config import settings


# =================================================
# ChromaDB Client
# =================================================

client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_PATH
)


# =================================================
# Get Collection
# =================================================

collection = client.get_collection(
    name="lesson_embeddings"
)


# =================================================
# Check Mathematics Records
# =================================================

results = collection.get(
    where={
        "subject": "mathematics"
    },
    include=[
        "metadatas"
    ]
)

print(
    f"Found {len(results['ids'])} mathematics chunks."
)

for i, metadata in enumerate(results["metadatas"]):
    print(
        results["ids"][i],
        metadata
    )


# =================================================
# Delete Mathematics
# =================================================

if results["ids"]:

    collection.delete(
        ids=results["ids"]
    )

    print(
        f"\n✅ Deleted {len(results['ids'])} mathematics chunks."
    )

else:

    print(
        "\n⚠️ No mathematics records found."
    )


# =================================================
# Verify
# =================================================

remaining = collection.get(
    where={
        "subject": "mathematics"
    },
    include=[
        "metadatas"
    ]
)

print(
    f"Remaining mathematics chunks: {len(remaining['ids'])}"
)