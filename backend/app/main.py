# backend/app/main.py

from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.vector_store import get_vector_store, get_embeddings, ingest_data
from groq import Groq
import os
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import Request, FastAPI, HTTPException

# --- App Initialization ---
app = FastAPI()

# --- CORS Setup ---
origins = [
    "http://localhost:3000",                  # your local Next.js dev server
    "https://ai-chatbot-1-psi.vercel.app",    # your Vercel-hosted frontend
] # Allow all for now (better to restrict later!)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static Files Mount ---
app.mount(
    "/data",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../data")),
    name="data",
)

# --- Globals ---
vector_db = None
embedding_model = None
groq_client = None

# --- Startup Events ---
@app.on_event("startup")
def startup_event():
    global vector_db, embedding_model, groq_client

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

# --- Health Check ---
@app.head("/")
def health_check():
    return Response(status_code=200)

# --- Root Route ---
@app.get("/")
def read_root():
    return {"message": "Chatbot is live!"}

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# --- Constants ---
SYSTEM_PROMPT = """
You are NutriBot, an AI expert on nutrition of Fruits and vegetables.
Answer the user's question based on the provided context.
If the answer isn't found in the context, respond exactly:
“My knowledge is based on my Nutrition of Fruits & Vegetable documents; I couldn't find a direct answer there. Here's what I can offer from my general expertise:..…”
""".strip()

# --- Chat Endpoint ---
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):



    # 1. Embed user query and search
    q_vec = embedding_model.embed_query(request.message)
    
    docs = vector_db.similarity_search_by_vector(q_vec, k=5)
    print(f"🔍 Found {len(docs)} relevant documents.")

    for i, doc in enumerate(docs, start=1):
        print(f"Chunk #{i} metadata → {doc.metadata}")
    

    if not docs:
        return {"reply": "I couldn't find anything relevant in my documents."}

    # 2. Build context
    context = "\n\n".join(doc.page_content for doc in docs)

    # 3. Call Groq LLM
    resp = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": context},
            {"role": "user",   "content": request.message},
        ],
        max_tokens=100,  # Limit response length
    )
    answer = resp.choices[0].message.content

    # 4. Build References
    references = []
    pages = []

    for doc in docs:
        first_doc = docs[0]
        fname = first_doc.metadata.get("source", "unknown.pdf")
        page = first_doc.metadata.get("page", 1)
        pages.append(page)
        base = str(req.base_url).rstrip("/")
        url = f"{base}/data/{fname}#page={page}"
        references.append(f"[{fname}]({url})")

    first_page = pages[0]
    first_ref = references[0]

    # 5. Full Reply
    full_reply = (
        f"{answer}\n\n"
        f"**References:**\n"
        f"Page No: {first_page}\n\n"
        f"{first_ref}"
    )

    return {"reply": full_reply}
