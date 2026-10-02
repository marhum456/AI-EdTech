from pathlib import Path

import fitz
from fastapi import UploadFile

from app.config import settings
from app.services.embedding_service import embedding_service
from app.services.vector_service import vector_service


# =====================================================
# Lesson Upload Service
# =====================================================

class LessonUploadService:
    """
    Handles complete lesson PDF ingestion.

    Flow:

        PDF Upload
            ↓
        Save PDF
            ↓
        Extract Text
            ↓
        Create Chunks
            ↓
        Generate Embeddings
            ↓
        Replace existing lesson chunks
            ↓
        Store new chunks in ChromaDB
    """

    # =================================================
    # Upload Lesson
    # =================================================

    async def upload_lesson(
        self,
        subject: str,
        course: str,
        lesson: str,
        file: UploadFile
    ):

        # -------------------------------------------------
        # 1. Validate input
        # -------------------------------------------------

        if not subject:
            raise ValueError(
                "Subject is required."
            )

        if not course:
            raise ValueError(
                "Course is required."
            )

        if not lesson:
            raise ValueError(
                "Lesson is required."
            )

        if not file:
            raise ValueError(
                "PDF file is required."
            )

        if not file.filename:
            raise ValueError(
                "PDF filename is missing."
            )

        if not file.filename.lower().endswith(".pdf"):
            raise ValueError(
                "Only PDF files are allowed."
            )

        # -------------------------------------------------
        # 2. Create upload directory
        # -------------------------------------------------

        upload_folder = Path(
            settings.UPLOAD_FOLDER
        )

        subject_folder = (
            upload_folder / subject
        )

        subject_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        # -------------------------------------------------
        # 3. Save PDF
        # -------------------------------------------------

        pdf_path = (
            subject_folder /
            file.filename
        )

        file_content = await file.read()

        if not file_content:
            raise ValueError(
                "Uploaded PDF is empty."
            )

        with open(
            pdf_path,
            "wb"
        ) as output_file:

            output_file.write(
                file_content
            )

        print("\n===================================")
        print("PDF SAVED")
        print("===================================")
        print(
            f"Path: {pdf_path}"
        )
        print(
            f"Size: {len(file_content)} bytes"
        )
        print("===================================\n")

        # -------------------------------------------------
        # 4. Extract PDF text
        # -------------------------------------------------

        pages = self.extract_pdf_text(
            pdf_path
        )

        if not pages:
            raise ValueError(
                "No text could be extracted from the PDF."
            )

        # -------------------------------------------------
        # 5. Create chunks
        # -------------------------------------------------

        chunks = self.create_chunks(
            pages
        )

        if not chunks:
            raise ValueError(
                "No chunks were created from the PDF."
            )

        print(
            f"📄 Extracted pages: {len(pages)}"
        )

        print(
            f"🧩 Created chunks: {len(chunks)}"
        )

        # -------------------------------------------------
        # 6. Create metadata
        # -------------------------------------------------

        metadata = []

        for index in range(
            len(chunks)
        ):

            metadata.append({

                # IMPORTANT:
                # Keep the exact values received
                # from Moodle/frontend.

                "subject": subject,

                "course": course,

                "lesson": lesson,

                "chunk_number": index + 1,

                "source": file.filename
            })

        # -------------------------------------------------
        # 7. Generate embeddings
        # -------------------------------------------------

        embeddings = (
            embedding_service.embed_documents(
                chunks
            )
        )

        if not embeddings:
            raise ValueError(
                "Failed to generate embeddings."
            )

        if len(embeddings) != len(chunks):
            raise ValueError(
                "Number of embeddings does not "
                "match number of chunks."
            )

        print(
            f"🧠 Generated embeddings: "
            f"{len(embeddings)}"
        )

        # -------------------------------------------------
        # 8. Replace existing lesson in ChromaDB
        # -------------------------------------------------

        replacement_result = (
            vector_service.replace_lesson(
                chunks=chunks,
                embeddings=embeddings,
                metadata=metadata
            )
        )

        deleted_chunks = (
            replacement_result["deleted_chunks"]
        )

        added_chunks = (
            replacement_result["added_chunks"]
        )

        print("\n===================================")
        print("CHROMADB INGESTION COMPLETED")
        print("===================================")
        print(
            f"Subject: {subject}"
        )
        print(
            f"Course: {course}"
        )
        print(
            f"Lesson: {lesson}"
        )
        print(
            f"Old chunks deleted: {deleted_chunks}"
        )
        print(
            f"New chunks added: {added_chunks}"
        )
        print("===================================\n")

        # -------------------------------------------------
        # 9. Return result
        # -------------------------------------------------

        if deleted_chunks > 0:

            message = (
                "Existing lesson replaced successfully "
                "with the new PDF."
            )

        else:

            message = (
                "New lesson processed and stored "
                "in ChromaDB."
            )

        return {

            "filename":
                file.filename,

            "file_path":
                str(pdf_path),

            "subject":
                subject,

            "course":
                course,

            "lesson":
                lesson,

            "chunks_created":
                len(chunks),

            "old_chunks_deleted":
                deleted_chunks,

            "new_chunks_added":
                added_chunks,

            "message":
                message
        }

    # =================================================
    # Extract PDF Text
    # =================================================

    def extract_pdf_text(
        self,
        pdf_path: Path
    ):

        pages = []

        try:

            document = fitz.open(
                pdf_path
            )

            for page in document:

                text = page.get_text(
                    "text"
                )

                text = text.strip()

                if text:
                    pages.append(
                        text
                    )

            document.close()

        except Exception as error:

            raise ValueError(
                f"Failed to read PDF: {error}"
            )

        return pages

    # =================================================
    # Create Chunks
    # =================================================

    def create_chunks(
        self,
        pages,
        chunk_size=1500,
        chunk_overlap=200
    ):
        """
        Split extracted text into chunks.
        """

        full_text = "\n\n".join(
            pages
        ).strip()

        if not full_text:
            return []

        chunks = []

        start = 0

        text_length = len(
            full_text
        )

        while start < text_length:

            end = min(
                start + chunk_size,
                text_length
            )

            chunk = (
                full_text[start:end]
                .strip()
            )

            if chunk:
                chunks.append(
                    chunk
                )

            if end >= text_length:
                break

            start = (
                end - chunk_overlap
            )

        return chunks


# =====================================================
# Singleton Instance
# =====================================================

lesson_upload_service = (
    LessonUploadService()
)