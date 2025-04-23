# backend/app/text_splitter.py
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(docs: dict[str, str], chunk_size=1000, chunk_overlap=100) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = []
    for doc_id, text in docs.items():
        doc_chunks = splitter.split_text(text)
        for i, chunk in enumerate(doc_chunks):
            chunks.append({
                "id": f"{doc_id}-{i}",
                "text": chunk,
                "metadata": {"source": doc_id, "chunk": i}
            })
    return chunks
