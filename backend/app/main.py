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




app = FastAPI()



# CORS setup
origins = [
    "http://localhost:3000",                  # for local development
 
    "https://ai-chatbot-1-psi.vercel.app",  # Your frontend domain
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.mount(
    "/data",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../data")),
    name="data",
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

SYSTEM_PROMPT = """
You are NutriBot, an AI expert on nutrition of Fruits and vegetables.
Answer the user's question based on the provided context.
If the answer isn't found in the context, respond exactly:
“My knowledge is based on my Nutrition of Fruits & Vegetable documents; I couldn't find a direct answer there. Here's what I can offer from my general expertise:..…”
""".strip()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    # 1) Retrieve relevant chunks
    q_vec   = embedding_model.embed_query(request.message)
    docs    = vector_db.similarity_search_by_vector(q_vec, k=5)

    # 2) Build “context” text only (no citations in the prompt)
    context = "\n\n".join(doc.page_content for doc in docs)

    # 3) Call the LLM with plain context
    resp = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": context},
            {"role": "user",   "content": request.message},
        ]
    )
    answer = resp.choices[0].message.content

    # 4) Build a “References” list from the exact docs we used
    references = []
    for doc in docs:
        fname = doc.metadata.get("source", "unknown.pdf")
        page  = doc.metadata.get("page", 1)
        base  = str(req.base_url).rstrip("/")
        url   = f"{base}/data/{fname}#page={page}"
        references.append(f"[{fname}]({url})")

    # 5) Return answer + a References section
    full_reply = (f"{answer}\n\n"
        f"**References:**\n"
        f"Page No: {page}\n\n"
        f"{references[0] if references else ''}"
    )
    return {"reply": full_reply}

@app.head("/")
def health_check():
    from fastapi.responses import Response
    return Response(status_code=200)
