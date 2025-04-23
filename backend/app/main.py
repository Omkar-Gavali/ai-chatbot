# backend/app/main.py (excerpt)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .vector_store import collection
from .embedder import get_embeddings
from groq import Groq
import os

app = FastAPI()
groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
# Reuse the same adapter
query_embedding_fn = create_langchain_embedding(get_embeddings())

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.on_event("startup")
def startup_event():
    from .indexer import index_pdfs
    index_pdfs(folder="backend/data")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # 1. Embed the query
        q_emb = query_embedding_fn([request.message])[0]

        # 2. Retrieve relevant PDF chunks
        results = collection.query(
            query_embeddings=[q_emb],
            n_results=3
        )
        contexts = "\n\n".join(results["documents"][0])

        # 3. Call Groq LLM with context
        messages = [
            {"role": "system",  "content": contexts},
            {"role": "user",    "content": request.message},
        ]
        resp = groq.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192"
        )
        return {"reply": resp.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
