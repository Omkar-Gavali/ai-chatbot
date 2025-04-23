# backend/app/vector_store.py

import os
import fitz  # PyMuPDF
import json
import logging
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import PDF_PATH, PERSIST_DIRECTORY, CHROMA_COLLECTION_NAME





# Logging
logging.basicConfig(level=logging.INFO)

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")



def process_pdf(pdf_path):
    docs = []
    pdf_document = fitz.open(pdf_path)
    file_name = os.path.basename(pdf_path)

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text("text")
        if text.strip():
            docs.append({
                "content": text,
                "metadata": {"page": page_num + 1, "file_name": file_name}
            })
    return docs

def process_json(json_path):
    docs = []
    file_name = os.path.basename(json_path)
    with open(json_path, "r") as file:
        data = json.load(file)
        for idx, item in enumerate(data):
            docs.append({
                "content": json.dumps(item),
                "metadata": {"id": idx + 1, "file_name": file_name}
            })
    return docs

def split_documents(docs, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.create_documents(
        texts=[doc["content"] for doc in docs],
        metadatas=[doc["metadata"] for doc in docs]
    )

def ingest_data():
    logging.info(f"📥 Ingesting data from {PDF_PATH} ")
    vector_db = init_vector_store()

    pdf_docs = process_pdf(PDF_PATH)
    
    all_docs = pdf_docs 

    if not all_docs:
        logging.warning("No documents found! Check file paths.")
        return vector_db

    split_docs = split_documents(all_docs)
    vector_db.add_documents(split_docs)
    vector_db.persist()
    return vector_db

# vector_store.py


def get_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )
