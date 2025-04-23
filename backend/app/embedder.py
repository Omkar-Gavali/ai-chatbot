# backend/app/embedder.py
#from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from app.config import PERSIST_DIRECTORY, CHROMA_COLLECTION_NAME

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

embeddings = get_embeddings()
collection = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    collection_name=CHROMA_COLLECTION_NAME,
    embedding_function=embeddings
)
