# backend/app/embedder.py
from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    """
    Returns a LangChain embedding instance
    using a local sentence-transformers model.
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={"device": "cpu"},            # or "cuda" if available
        encode_kwargs={"normalize_embeddings": True} # recommended for cosine sims
    )
