# backend/app/indexer.py
from .pdf_loader import load_pdfs
from .text_splitter import chunk_documents
from .vector_store import collection

def index_pdfs(folder: str):
    # Load raw PDF texts
    docs = load_pdfs(folder)

    # Split into overlapping chunks
    chunks = chunk_documents(docs)

    # Prepare lists
    texts     = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids       = [c["id"] for c in chunks]

    # Chroma will call chroma_ef(texts) under the hood
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )
    collection.persist()  # save to disk
