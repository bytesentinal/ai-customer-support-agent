```markdown
# AI Customer Support Agent

A RAG-powered customer support chatbot that answers questions from your own documents. Built with FastAPI, LangChain, ChromaDB, and Groq.

## Features

- 📄 Answers from your documents (RAG via ChromaDB)
- ⚡ Fast inference via Groq (llama-3.3-70b)
- 🔌 REST API with `/chat`, `/reset`, `/health` endpoints
- 🐳 Fully Dockerized — runs anywhere

## Tech Stack

- **Python 3.13** · **FastAPI** · **LangChain** · **ChromaDB** · **Groq API** · **Docker**

## Project Structure

```
├── app/
│   ├── main.py       # FastAPI routes
│   ├── agent.py      # RAG chain + Groq LLM
│   ├── ingest.py     # Document ingestion into ChromaDB
│   └── config.py     # Environment config
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Getting Started

### 1. Clone & configure
```bash
git clone https://github.com/YOUR_USERNAME/ai-support-agent.git
cd ai-support-agent
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### 2. Run with Docker
```bash
docker-compose up --build
```

### 3. Ingest your documents
```bash
docker-compose exec app python app/ingest.py
```

### 4. Test the API
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What services do you offer?"}'
```

## API Endpoints

| Method | Endpoint  | Description              |
|--------|-----------|--------------------------|
| POST   | `/chat`   | Send a message           |
| POST   | `/reset`  | Reset conversation       |
| GET    | `/health` | Health check             |

## Environment Variables

```
GROQ_API_KEY=your_key_here
```
