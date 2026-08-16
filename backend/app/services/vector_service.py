import chromadb

from app.config import settings


# =================================================
# ChromaDB Client
# =================================================

client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_PATH
)


# =================================================
# ChromaDB Collection
# =================================================

collection = client.get_or_create_collection(
    name="lesson_embeddings"
)


# =================================================
# Vector Service
# =================================================

class VectorService:
    """
    Handles storage and retrieval from ChromaDB.
    """

    # =================================================
    # Add Chunks
    # =================================================

    def add_chunks(
        self,
        chunks,
        embeddings,
        metadata
    ):

        # -------------------------------------------------
        # Create globally unique IDs
        # -------------------------------------------------

        ids = []

        for i, meta in enumerate(metadata):

            subject = meta["subject"]
            course = meta["course"]
            lesson = meta["lesson"]

            chunk_id = (
                f"{subject}_"
                f"{course}_"
                f"{lesson}_"
                f"chunk_{i + 1}"
            )

            ids.append(chunk_id)

        # -------------------------------------------------
        # Store in ChromaDB
        # -------------------------------------------------

        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata
        )

        print(
            f"✅ Added {len(chunks)} chunks to ChromaDB."
        )

    # =================================================
    # Semantic Search
    # =================================================

    def search(
        self,
        query_embedding,
        n_results=5,
        where=None
    ):

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )

        return results

    # =================================================
    # Get All Lesson Chunks
    # =================================================

    def get_lesson_chunks(
        self,
        subject,
        course,
        lesson
    ):
        """
        Retrieve ALL chunks for a specific lesson.

        Used for quiz generation.
        No semantic search is performed here.
        """

        results = collection.get(
            where={
                "$and": [
                    {
                        "subject": subject
                    },
                    {
                        "course": course
                    },
                    {
                        "lesson": lesson
                    }
                ]
            },
            include=[
                "documents",
                "metadatas"
            ]
        )

        return results


# =================================================
# Singleton Instance
# =================================================

vector_service = VectorService()