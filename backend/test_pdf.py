from app.services.pdf_service import (
    extract_text_from_pdf,
    clean_text,
)

pdf_path = r"../uploads/Javascript/JavaScript Fundamentals.pdf"

text = extract_text_from_pdf(pdf_path)
text = clean_text(text)

print("\n===== Extracted Text =====\n")
print(text[:2000])  # print first 2000 characters
print("\n==========================\n")