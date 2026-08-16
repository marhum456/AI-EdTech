from pathlib import Path

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import create_chunks
from app.services.embedding_service import embedding_service
from app.services.vector_service import vector_service

BASE_DIR = Path(__file__).resolve().parent.parent

pdf_path = BASE_DIR / "uploads" / "web_developement" / "JavaScript Fundamentals.pdf"

text = extract_text_from_pdf(pdf_path)

chunks = create_chunks(text)

embeddings = embedding_service.embed_documents(chunks)

metadata = []

for i in range(len(chunks)):
    metadata.append(
        {
            "subject": "web_developement",
            "course": "javascript",
            "lesson": "lesson_1",
            "chunk_number": i + 1,
            "source": "JavaScript Fundamentals.pdf",
        }
    )
    
vector_service.add_chunks(
    chunks,
    embeddings,
    metadata
)

print("\n✅ Chunks stored in ChromaDB successfully!")
print(f"Stored Chunks: {len(chunks)}")