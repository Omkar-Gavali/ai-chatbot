# backend/app/vector_store.py

import os
import logging
from typing import List
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from app.config import PDF_PATH, PERSIST_DIRECTORY, CHROMA_COLLECTION_NAME
from typing import List
from PyPDF2 import PdfReader
from langchain.schema import Document

from langchain.schema import Document



logging.basicConfig(level=logging.INFO)

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")



def read_pdfs(folder: str) -> List[Document]:
    docs = []
    for fname in os.listdir(folder):
        if fname.lower().endswith(".pdf"):
            path = os.path.join(folder, fname)
            reader = PdfReader(path)

            for page_num, page in enumerate(reader.pages):
                content = page.extract_text() or ""
                if content.strip():  # Only add non-empty pages
                    docs.append(Document(
                        page_content=content,
                        metadata={
                            "source": fname,
                            "page": page_num + 1  # pages are 1-indexed
                        }
                    ))
    return docs



def split_documents(docs: List[Document], chunk_size=1000, chunk_overlap=100) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)


def init_vector_store():
    return Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=get_embeddings()
    )

def ingest_data():
    # If the persistence folder already exists and has data, skip re-building
    logging.info(f"🔍 Loading vector store from {PERSIST_DIRECTORY}")
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
