# backend/app/main.py

from fastapi.responses import Response
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.vector_store import get_vector_store, get_embeddings, ingest_data
from groq import Groq
import os
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# CORS setup
origins = [
    "https://ai-chatbot-1-psi.vercel.app/",  # Your frontend domain
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Globals to initialize at startup
vector_db = None
embedding_model = None
groq_client = None  # 👈 Initialize later

@app.on_event("startup")
def startup_event():
    global vector_db, embedding_model, groq_client

    # Wrap ingestion in try/except to avoid crashing the app
    try:
        ingest_data()
        print("✅ Data ingestion completed.")
    except Exception as e:
        print(f"⚠️  Data ingestion failed: {e}")

    try:
        vector_db = get_vector_store()
        embedding_model = get_embeddings()
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        print("✅ Startup components initialized.")
    except Exception as e:
        print(f"❌ Startup initialization failed: {e}")

    


@app.get("/")
def read_root():
    return {"message": "Chatbot is live!"}

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        query = request.message
        query_vector = embedding_model.embed_query(query)
        results = vector_db.similarity_search_by_vector(query_vector, k=3)
        context = "\n\n".join(doc.page_content for doc in results)

        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": query}
        ]

        resp = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )
        return {"reply": resp.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.head("/")
def health_check():
    from fastapi.responses import Response
    return Response(status_code=200)
