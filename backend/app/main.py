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





app = FastAPI()


app.mount(
    "/data",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../data")),
    name="data",
)

# CORS setup
origins = [
    "http://localhost:3000",
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
        context_text = "\n\n".join(
        f"[{doc.metadata['source']} – page {doc.metadata.get('page', '?')}](/data/{doc.metadata['source']}#page={doc.metadata.get('page',1)})\n\n{doc.page_content}"
        for doc in results
        )


        # 1) DEFINE YOUR SYSTEM PROMPT HERE, AT MODULE LEVEL
        SYSTEM_PROMPT = """
        You are NutritionBot, an AI expert on nutrition and vegetables.

        If the user's question isn't answered by the supplied Nutrition & Vegetable materials, say:
        “I am NutriBot. My knowledge is based on  Nutrition and Vegetable documents, and I couldn't find a direct answer there.
        However, here's what I can offer from my general expertise: …”

        After your answer, always cite the document source(s) you used in this format at the end of your answer:

        [filename.pdf](https://<YOUR_BACKEND_URL>/data/filename.pdf)

        

        Your entire reply (including citations) must be **no more than 500 characters**.  
        """.strip()

        messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": context_text},
        {"role": "user",   "content": query}
        ]

        resp = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            max_completion_tokens= 90 # Set desired token limit

        )
        return {"reply": resp.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.head("/")
def health_check():
    from fastapi.responses import Response
    return Response(status_code=200)
