import chromadb

from app.config import settings

client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)

collection = client.get_or_create_collection(
    name="lesson_embeddings"
)


class VectorService:
    """
    Handles storage and retrieval from ChromaDB.
    """

    def add_chunks(
        self,
        chunks,
        embeddings,
        metadata
    ):
        ids = [f"chunk_{i}" for i in range(len(chunks))]

        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata
        )

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

    def get_lesson_chunks(
        self,
        subject,
        course,
        lesson
    ):
        """
        Retrieve ALL chunks for a specific lesson.
        Used for quiz generation (no semantic search).
        """

        results = collection.get(
            where={
                "$and": [
                    {"subject": subject},
                    {"course": course},
                    {"lesson": lesson}
                ]
            },
            include=["documents", "metadatas"]
        )

        return results


vector_service = VectorService()