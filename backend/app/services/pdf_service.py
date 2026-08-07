import re
import fitz  # PyMuPDF


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text for RAG.
    """

    # Remove page numbers on their own line
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)

    # Remove bullet-only lines
    text = re.sub(r"^\s*[•▪●◦]+\s*$", "", text, flags=re.MULTILINE)

    # Replace multiple spaces/tabs with one space
    text = re.sub(r"[ \t]+", " ", text)

    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return clean_text(text)