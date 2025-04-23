# backend/app/pdf_loader.py
from pypdf import PdfReader
import os

def load_pdfs(text_folder: str) -> dict[str, str]:
    """Return a mapping from filename to extracted text."""
    docs = {}
    for fname in os.listdir(text_folder):
        if fname.lower().endswith(".pdf"):
            path = os.path.join(text_folder, fname)
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            docs[fname] = text
    return docs
