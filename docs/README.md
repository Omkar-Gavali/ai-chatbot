# AI Chatbot Demo

A full-stack AI chatbot using the Groq LLM API, demonstrating nutrition and beauty product Q&A.

## Tech Stack
- **Backend**: Python + FastAPI
- **Frontend**: Next.js + React + Tailwind CSS
- **AI**: Groq LLM API + Pinecone (RAG)
- **Hosting**: Render (backend), Vercel (frontend)

## Setup
1. Clone repo
2. Create `.env` files with your API keys
3. Start backend: `uvicorn app.main:app --reload`
4. Start frontend: `npm run dev`

## Directory Structure

├── backend/
│   ├── app/           # FastAPI application
│   ├── requirements.txt
│   ├── Dockerfile
├── frontend/
│   ├── pages/         # Next.js pages & API routes
│   ├── components/
│   ├── package.json
├── docs/
│   ├── README.md
│   └── rew.txt        # dev notes
├── .gitignore
└── README.md
