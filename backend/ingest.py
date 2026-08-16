from pathlib import Path
import argparse

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import create_chunks
from app.services.embedding_service import embedding_service
from app.services.vector_service import vector_service


# =================================================
# Base Directory
# =================================================

# ingest.py is inside:
# AI-EdTech/backend/
#
# parent      -> AI-EdTech/backend
# parent.parent -> AI-EdTech
#
# uploads is inside AI-EdTech/

BASE_DIR = Path(__file__).resolve().parent.parent


# =================================================
# Ingest PDF
# =================================================

def ingest_pdf(
    subject: str,
    course: str,
    lesson: str,
    pdf_name: str,
):

    print("\n==============================================")
    print("Starting PDF Ingestion")
    print("==============================================")

    print(f"Subject : {subject}")
    print(f"Course  : {course}")
    print(f"Lesson  : {lesson}")
    print(f"PDF     : {pdf_name}")

    # -------------------------------------------------
    # 1. Build PDF Path
    # -------------------------------------------------

    pdf_path = (
        BASE_DIR
        / "uploads"
        / subject
        / pdf_name
    )

    if not pdf_path.exists():

        raise FileNotFoundError(
            f"\n❌ PDF not found:\n{pdf_path}"
        )

    print(f"\n📄 PDF found: {pdf_path}")

    # -------------------------------------------------
    # 2. Extract Text
    # -------------------------------------------------

    print("\n📖 Extracting text...")

    text = extract_text_from_pdf(pdf_path)

    if not text or not text.strip():

        raise Exception(
            "❌ No text could be extracted from the PDF."
        )

    print("✅ Text extracted successfully.")

    # -------------------------------------------------
    # 3. Create Chunks
    # -------------------------------------------------

    print("\n✂️ Creating chunks...")

    chunks = create_chunks(text)

    if not chunks:

        raise Exception(
            "❌ No chunks were created."
        )

    print(f"✅ Created {len(chunks)} chunks.")

    # -------------------------------------------------
    # 4. Generate Embeddings
    # -------------------------------------------------

    print("\n🧠 Generating embeddings...")

    embeddings = embedding_service.embed_documents(
        chunks
    )

    if not embeddings:

        raise Exception(
            "❌ No embeddings were generated."
        )

    print("✅ Embeddings generated.")

    # -------------------------------------------------
    # 5. Create Metadata
    # -------------------------------------------------

    metadata = []

    for i in range(len(chunks)):

        metadata.append(
            {
                "subject": subject,
                "course": course,
                "lesson": lesson,
                "chunk_number": i + 1,
                "source": pdf_name,
            }
        )

    print("\n🏷️ Metadata created.")

    # -------------------------------------------------
    # 6. Store in ChromaDB
    # -------------------------------------------------

    print("\n💾 Storing chunks in ChromaDB...")

    vector_service.add_chunks(
        chunks,
        embeddings,
        metadata
    )

    # -------------------------------------------------
    # 7. Complete
    # -------------------------------------------------

    print("\n==============================================")
    print("✅ PDF INGESTION COMPLETED")
    print("==============================================")

    print(f"Subject       : {subject}")
    print(f"Course        : {course}")
    print(f"Lesson        : {lesson}")
    print(f"PDF           : {pdf_name}")
    print(f"Stored Chunks : {len(chunks)}")

    print("==============================================\n")


# =================================================
# Command Line Arguments
# =================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Ingest a course lesson PDF into ChromaDB."
    )

    parser.add_argument(
        "--subject",
        required=True,
        help="Subject name"
    )

    parser.add_argument(
        "--course",
        required=True,
        help="Course name"
    )

    parser.add_argument(
        "--lesson",
        required=True,
        help="Lesson name"
    )

    parser.add_argument(
        "--pdf",
        required=True,
        help="PDF filename"
    )

    args = parser.parse_args()

    ingest_pdf(
        subject=args.subject,
        course=args.course,
        lesson=args.lesson,
        pdf_name=args.pdf,
    )