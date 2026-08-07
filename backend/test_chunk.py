from pathlib import Path

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import create_chunks

BASE_DIR = Path(__file__).resolve().parent.parent

f_path = BASE_DIR / "uploads" / "Javascript" / "JavaScript Fundamentals.pdf"
pd
text = extract_text_from_pdf(pdf_path)

chunks = create_chunks(text)

print(f"\nTotal Chunks: {len(chunks)}\n")

for i, chunk in enumerate(chunks, start=1):
    print("=" * 60)
    print(f"Chunk {i}")
    print("=" * 60)
    print(chunk)
    print()