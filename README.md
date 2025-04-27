

# 🌟 NutriBot - AI Powered Nutrition Chatbot
Welcome to **NutriBot**, your go to assistant **trained on the nutritional properties of fruits and vegetables**. NutriBot excels at answering detailed questions such as _“Why does eating potato skin provide more iron than eating potato flesh?”_ by grounding every response in the source PDF data along with page numbre from that pdf.

---

## 🌐 Live Demo

👉 **Check out the live version here:**  [🔗 NutriBot ](https://ai-chatbot-1-psi.vercel.app/)

### 💬 Try Asking NutriBot

- **How does iron deficiency impact human health, including work capacity and immune function?**  
- **Why does eating potato skin provide more iron than eating potato flesh?**  
- **What are some primary dietary sources of iron in the American food supply?** 
- **How are the metabolic fates of copper and iron related?**
- **What causes fruits to turn brown after we cut them?**



<p align="center">
  <img src="./frontend/public/demo3.gif" alt="NutriBot Live Demo" width="600" />
</p>


---

### **NutriBot Data Source**

Vicente, A. R., Ortiz, C. M., Sozzi, G. O., Manganaris, G. A., & Crisosto, C. H. (2014). *Nutritional properties of fruits and vegetables*. In Postharvest Biology and Technology of Fruits, Vegetables, and Flowers (pp. 69–122). Elsevier. https://doi.org/10.1016/B978-0-12-408137-6.00005-3 :contentReference[oaicite:1]{index=1}

---
 # Key Features  
 - **AI-Powered Chat:** Conversational interface using Groq LLM API integrated via FastAPI, Scalable to **n** number of PDFs.  
 - **Document Embedding & Search:** Uses open source HuggingFace embeddings and Chroma vector store to index and retrieve PDF content.
 - **RetrievalAugmented Generation (RAG):** Combines semantic search from vector database with LLM responses for accurate, context-aware answers.  
 - **Dynamic Loading Animation:** Nutrition themed Lottie animations during inference for engaging feedback  
 - **Responsive UI:** Built with Next.js and Tailwind CSS, fully mobile responsive and accessible  
 - **Markdown & Links:** Bot replies support full Markdown including clickable links via `react-markdown` and `remark-gfm`. 
- **Source Referencing:** Every answer includes references with page numbers and direct links to the original document for full transparency.
 # Tech Stack  
 - **Backend:** Python • FastAPI • Uvicorn • Groq • LangChain • ChromaDB • PyMuPDF  
 - **Frontend:** Next.js v15 • React • Tailwind CSS • Framer Motion • Lottie-React  
 - **DevOps:** Docker • GitHub • Vercel • Google Cloud Run 

---

## 🛠️ Project Structure

- **Frontend**: [Next.js](https://nextjs.org/) deployed on [Vercel](https://vercel.com/)  
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) containerized on [GCP Cloud Run](https://cloud.google.com/run) using [Docker](https://www.docker.com/)  
- **Vector Database**: Chroma for document retrieval  
- **LLM API**: GROQ’s LLaMA 3 model  

---


# Getting Started (Local)  
## Prerequisites  
 - Python 3.10+  
 - Node.js ≥ 18 (via NVM or direct install)  
 - pnpm or npm  
 - Docker (for containerized setup)

## 🚀 How to Deploy Locally
### 1. Clone the Repo
```bash
git clone https://github.com/Omkar-Gavali/ai-chatbot.git
cd ai-chatbot
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Create a .env in backend/:
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run Backend

Place your PDF files in `backend/data/` and run: 
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Backend: `http://localhost:8000`

### 4. Frontend Setup
```bash
cd frontend
npm install

# Create .env.local in frontend/:
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CHAT_ENDPOINT=${NEXT_PUBLIC_API_URL}/chat
```

### 5. Run Frontend
```bash
npm run dev
```
Frontend: `http://localhost:3000`

---

## 🐳 Docker & GCP Cloud Run

### 1. Build Backend Image
```bash
cd backend
docker build -t ai-chatbot/backend .
```

### 2. Test Locally

```bash
cd backend
docker run -p 8000:8000 backend
```

### 3. Push to GCR
```bash
cd backend
gcloud auth configure-docker
docker tag nutribot-backend gcr.io/your-gcp-project-id/backend
docker push gcr.io/your-gcp-project-id/backend
```

### 4. Deploy to Cloud Run
```bash
gcloud run deploy nutribot-backend \
  --image gcr.io/your-gcp-project-id/ai-chatbot-backend \
  --platform managed \
  --region europe-west3 \
  --allow-unauthenticated \
  --port 8000
```





---

## 🌍 Vision & Impact

NutriBot is part of a movement:

- **Democratizing Knowledge**: Free nutritional insights Fruits and Vegetables.  
- **Responsible AI**: Context aware with fall back mechanism to ensure responses are only based on the documents provided . 
- **Scalable Architecture**: Ready for tomorrow’s multi document world.  
- **Positive AGI Future**: AI as a collaborator, not a replacement.

> “We must not only imagine a better future with AI. We must build it — with responsibility, passion, and relentless optimism.”

---

## 📈 Future Scope

- 📚 **Multi-PDF Support**: Unlimited document ingestion.
- 🔌 **Plugin Ecosystem:** Connect to live APIs (recipe databases, health trackers) for real-time personalization.  
  
- 🤖 **LLM Choice**: Swap models (LLaMA, GPT, Claude) with different parameters(top_k,temperature etc.)  
- 🔍 **Advanced Retrieval**: Hybrid semantic + keyword search.  
- 🌐 **Localization**: Multi-language Q&A.  
- ⚙️ **Offline LLMs**: Onpremise models for privacy.  
- 📊 **Knowledge Graphs**: Enhanced reasoning pipelines.
- 🔐 **Authentication**: User-specific personalization.
- ⚖️ **AI Safety & Ethics:** Integrate fairness and consent frameworks,

---

## ⚙️ Configuration Files

- **`requirements.txt`**: Python deps for backend.  
- **`Dockerfile`**: Container spec.  
- **`.env.example`**: Template env vars.

---

## 💖 Made with ❤️ for the Future

If you find this project inspiring, please ⭐ Star on GitHub and share with the world!

---

## 📜 License

MIT License © 2025


 # AI & AGI Vision  
 As AI/AGI progresses from pattern recognition to **real-world experience learning**, systems will autonomously generate data and refine themselves in situations. I foresee NutriBot evolving into a network of domain specific advisors nutrition, skincare, mental health contributing to a future where AI augments human well being at scale, democratizing access to expert guidance.  



 # Contributing  
 We welcome your ideas, whether it’s adding new PDF loaders, improving UI/UX, or experimenting with embedding models. Please **fork**, **commit**, and **open a pull request** your contributions drive NutriBot toward a healthier, AI-empowered world! 
 
## 📚 Knowledge Multiplier  
_"Every PDF you upload expands NutriBot’s ability to provide deeper, more connected nutritional insights. The future of personalized nutrition begins with the documents you share."_


 # Credits  
 Built with 💚 by **Omkar** — shaping AI for good, one delicious smoothie at a time!  
