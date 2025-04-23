# backend/app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.vector_store import get_vector_store, get_embeddings, ingest_data
from groq import Groq
import os

app = FastAPI()

groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
vector_db = None
embedding_model = None

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.on_event("startup")
def startup_event():
    global vector_db, embedding_model
    ingest_data()  # Build or update the vector DB from PDFs
    vector_db = get_vector_store()
    embedding_model = get_embeddings()

@app.get("/")
def root():
    return {"message": "Chatbot is live!"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        query = request.message
        query_vector = embedding_model.embed_query(query)

        # search
        results = vector_db.similarity_search_by_vector(query_vector, k=3)
        context = "\n\n".join(doc.page_content for doc in results)

        # format and call Groq
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": query}
        ]

        resp = groq.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )
        return {"reply": resp.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
