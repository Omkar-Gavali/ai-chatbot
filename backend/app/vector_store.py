from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import chromadb

# Load HuggingFace embedding model
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Initialize vector store and return the collection
def init_vector_store():
    embeddings = get_embeddings()
    client = chromadb.PersistentClient(path="chroma_data")
    return Chroma(
        client=client,
        collection_name="nutrition_beauty_demo",
        embedding_function=embeddings
    )

# Initialize the collection
collection = init_vector_store()
