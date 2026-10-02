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
    Handles storage, replacement, and retrieval
    of lesson chunks in ChromaDB.
    """

    # =================================================
    # Delete Existing Lesson
    # =================================================

    def delete_lesson(
        self,
        subject,
        course,
        lesson
    ):
        """
        Delete all existing chunks for a specific lesson.

        This is used when a teacher uploads a new version
        of an existing lesson.
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
                "metadatas"
            ]
        )

        existing_ids = results.get("ids", [])

        if existing_ids:

            collection.delete(
                ids=existing_ids
            )

            print(
                f"🗑️ Deleted {len(existing_ids)} existing "
                f"chunks for "
                f"{subject}/{course}/{lesson}"
            )

            return len(existing_ids)

        print(
            f"ℹ️ No existing chunks found for "
            f"{subject}/{course}/{lesson}"
        )

        return 0

    # =================================================
    # Replace Lesson
    # =================================================

    def replace_lesson(
        self,
        chunks,
        embeddings,
        metadata
    ):
        """
        Replace an existing lesson with a new version.

        Process:

        1. Identify subject/course/lesson.
        2. Delete existing chunks.
        3. Add the new chunks.
        """

        if not metadata:
            raise ValueError(
                "Metadata cannot be empty."
            )

        # -------------------------------------------------
        # Get lesson identity from metadata
        # -------------------------------------------------

        subject = metadata[0]["subject"]
        course = metadata[0]["course"]
        lesson = metadata[0]["lesson"]

        # -------------------------------------------------
        # Delete old lesson chunks
        # -------------------------------------------------

        deleted_count = self.delete_lesson(
            subject=subject,
            course=course,
            lesson=lesson
        )

        # -------------------------------------------------
        # Add new lesson chunks
        # -------------------------------------------------

        added_count = self.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
            metadata=metadata
        )

        print(
            f"🔄 Lesson replaced successfully: "
            f"{subject}/{course}/{lesson} | "
            f"Deleted: {deleted_count} | "
            f"Added: {added_count}"
        )

        return {
            "deleted_chunks": deleted_count,
            "added_chunks": added_count
        }

    # =================================================
    # Add Chunks
    # =================================================

    def add_chunks(
        self,
        chunks,
        embeddings,
        metadata
    ):
        """
        Add new lesson chunks to ChromaDB.
        """

        if not chunks:
            raise ValueError(
                "Chunks cannot be empty."
            )

        if not embeddings:
            raise ValueError(
                "Embeddings cannot be empty."
            )

        if not metadata:
            raise ValueError(
                "Metadata cannot be empty."
            )

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

        return len(chunks)

    # =================================================
    # Semantic Search
    # =================================================

    def search(
        self,
        query_embedding,
        n_results=5,
        where=None
    ):
        """
        Perform semantic search in ChromaDB.
        """

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