# backend/app/vector_store.py

import os
import logging
from typing import List
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from app.config import PDF_PATH, PERSIST_DIRECTORY, CHROMA_COLLECTION_NAME

logging.basicConfig(level=logging.INFO)

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def read_pdfs(folder: str) -> List[dict]:
    docs = []
    for fname in os.listdir(folder):
        if fname.lower().endswith(".pdf"):
            path = os.path.join(folder, fname)
            reader = PdfReader(path)
            content = ""
            for page in reader.pages:
                content += page.extract_text() or ""
            docs.append({
                "content": content,
                "metadata": {"source": fname}
            })
    return docs

def split_documents(docs: List[dict], chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = [doc["content"] for doc in docs]
    metadatas = [doc["metadata"] for doc in docs]
    return splitter.create_documents(texts=texts, metadatas=metadatas)

def init_vector_store():
    return Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=get_embeddings()
    )

def ingest_data():
    # If the persistence folder already exists and has data, skip re-building
    if os.path.isdir(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
        logging.info("⚠️  Found existing Chroma data—skipping ingestion.")
        return init_vector_store()

    logging.info(f"📥 Ingesting PDFs from {PDF_PATH}")
    docs = read_pdfs(PDF_PATH)
    if not docs:
        logging.warning("❌ No PDFs found.")
        return

    splits = split_documents(docs)
    store = init_vector_store()
    store.add_documents(splits)
    store.persist()
    logging.info("✅ Ingestion complete.")
    return store

def get_vector_store():
    return init_vector_store()
