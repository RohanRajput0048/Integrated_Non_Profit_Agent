# 🤖 Non Profit Agent

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

**Non Profit Agent** is an enterprise-grade, Microservices-based training platform designed to simulate high-stakes donor interactions for non-profit staff. It utilizes **Agentic AI** to autonomously triage incoming donor communications and **Retrieval-Augmented Generation (RAG)** to dynamically generate legally compliant, mathematically graded training quizzes.

## ✨ Key Features
*   **Agentic Triage Workflow:** Autonomously calculates emotional tone and financial risk from raw emails to assign Urgency Levels (High/Medium/Low) and SLA deadlines.
*   **Zero-Hallucination RAG Pipeline:** Mathematical Vector Embeddings (ChromaDB) restrict the Google Gemini LLM, forcing it to grade trainees based strictly on private organizational PDFs.
*   **Dynamic Quiz Generation:** Synthesizes 5-question multiple-choice training scenarios tailored to the parsed donor email.
*   **Cloud-Ready DevOps:** Fully containerized via Docker and automated via a GitHub Actions CI/CD pipeline.

## 🛠️ Technology Stack
*   **Frontend:** Streamlit (State-managed GUI)
*   **Backend:** FastAPI & Uvicorn (Asynchronous HTTP Routing)
*   **LLM Integration:** Google Gemini 2.5 Flash API (`google-genai` SDK)
*   **RAG Infrastructure:** LangChain (PyPDFLoader) & ChromaDB (Persistent SQLite Vector Database)
*   **DevOps:** Docker, Docker Compose, GitHub Actions

## 📂 Project Structure
```text
├── backend/
│   ├── api.py           # FastAPI Router & Endpoints
│   ├── models.py        # Pydantic Data Validation Schemas
│   ├── database.py      # ChromaDB Vector Embeddings & PDF Ingestion
│   └── llm_service.py   # Core Prompt Engineering & Agentic Reasoning
├── frontend/
│   └── app.py           # Streamlit User Interface
├── data/                # Directory for raw PDF policy documents
├── .github/workflows/
│   └── ci.yml           # CI/CD automation pipeline
├── docker-compose.yml   # Multi-container orchestration
├── Dockerfile           # Linux container build instructions
└── requirements.txt     # Python dependencies
```

## 🚀 Installation & Setup

### Prerequisites
*   Python 3.10+ (If running locally)
*   Docker Desktop (If running containerized)
*   A Google Gemini API Key

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/non-profit-agent.git
cd non-profit-agent
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory and add your API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Deploy using Docker (Recommended)
This command will simultaneously build and boot both the FastAPI backend and Streamlit frontend.
```bash
docker-compose up --build
```
*   The UI will be accessible at: `http://localhost:8501`
*   The API will be accessible at: `http://localhost:8000`

### 4. Deploy Locally (Without Docker)
Open two separate terminals.
**Terminal 1 (Backend):**
```bash
pip install -r requirements.txt
uvicorn backend.api:app --reload
```
**Terminal 2 (Frontend):**
```bash
streamlit run frontend/app.py
```

## 📈 Future Scope
*   **Multi-Modal Ingestion:** Integration with Whisper API to triage audio voicemails.
*   **Persistent Analytics:** Transitioning from ephemeral session state to a PostgreSQL database for tracking long-term trainee performance metrics.
*   **Multi-Agent Orchestration:** Upgrading from linear prompt-routing to frameworks like CrewAI for complex legal and financial sub-agent task delegation.
