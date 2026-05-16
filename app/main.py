from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import build_agent, ask, reset_memory

app = FastAPI(title="AI Support Agent", version="1.0")

retriever, llm = build_agent()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/health")
def health():
    return {"status": "running"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    reply = ask(retriever, llm, request.message)
    return ChatResponse(reply=reply)

@app.post("/reset")
def reset():
    reset_memory()
    return {"status": "Memory cleared."}