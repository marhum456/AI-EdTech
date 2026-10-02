
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
# Check web_developement Records
# =================================================

results = collection.get(
    where={
        "course": "web_developement"
    },
    include=[
        "metadatas"
    ]
)

print(
    f"Found {len(results['ids'])} "
    f"web_developement chunks."
)


# =================================================
# Display Records Before Deletion
# =================================================

for i, metadata in enumerate(results["metadatas"]):

    print(
        results["ids"][i],
        metadata
    )


# =================================================
# Delete web_developement Records
# =================================================

if results["ids"]:

    collection.delete(
        ids=results["ids"]
    )

    print(
        f"\n✅ Deleted {len(results['ids'])} "
        f"web_developement chunks."
    )

else:

    print(
        "\n⚠️ No web_developement records found."
    )


# =================================================
# Verify Deletion
# =================================================

remaining = collection.get(
    where={
        "course": "web_developement"
    },
    include=[
        "metadatas"
    ]
)

print(
    f"Remaining web_developement chunks: "
    f"{len(remaining['ids'])}"
)


# =================================================
# Finished
# =================================================

print(
    "\n==============================================="
)

print(
    "✅ web_developement cleanup completed."
)

print(
    "==============================================="
)
