"""
API FastAPI — expose le service multi-agent
100 % LangChain
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI
from pydantic import BaseModel

from agents.orchestration import run_multi_agent

app = FastAPI(
    title="Conseiller Voyage Maroc",
    description="Multi-agent LangChain pur",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"


class ChatResponse(BaseModel):
    answer: str
    session_id: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    answer = run_multi_agent(req.message, session_id=req.session_id)
    return ChatResponse(answer=answer, session_id=req.session_id)