from .pdf_loader import load_pdfs
from .text_splitter import chunk_documents
from app.vector_store import get_vector_store

def index_pdfs(folder: str):
    # Load raw PDF texts
    docs = load_pdfs(folder)

    # Split into overlapping chunks
    chunks = chunk_documents(docs)

    # Initialize the vector DB
    collection = get_vector_store()

    # Prepare lists
    texts     = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids       = [c["id"] for c in chunks]

    # Add to Chroma
    collection.add_documents(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )
    collection.persist()
