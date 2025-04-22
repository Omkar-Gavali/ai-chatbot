from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv

# Load .env variables (like API key)
load_dotenv()

app = FastAPI()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Request model
class ChatRequest(BaseModel):
    message: str

# Response model
class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Chat with Groq
        groq_response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": request.message}],
            model="llama3-8b-8192"
        )
        return {"reply": groq_response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
