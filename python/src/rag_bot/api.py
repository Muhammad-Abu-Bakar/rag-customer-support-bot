"""HTTP interface to the support agent.

Run locally:  uvicorn rag_bot.api:app --reload
"""

import logging
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from rag_bot.agent import ask
from rag_bot.config import ConfigError, load_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG Support Bot",
    description="Answers questions from Stripe's webhooks documentation, with citations.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500, examples=[
        "How do I verify a webhook signature?"
    ])


class AskResponse(BaseModel):
    question: str
    answer: str
    elapsed_seconds: float


@app.get("/health")
def health() -> dict:
    """Liveness check. Confirms config loads without calling any external API."""
    try:
        settings = load_settings()
    except ConfigError as exc:
        raise HTTPException(status_code=503, detail=f"Config error: {exc}") from exc

    return {
        "status": "ok",
        "index": settings.pinecone_index_name,
        "namespace": settings.pinecone_namespace,
        "chat_model": settings.chat_model,
    }


@app.post("/ask", response_model=AskResponse)
def ask_endpoint(request: AskRequest) -> AskResponse:
    """Answer a question using only the ingested documentation."""
    started = time.monotonic()

    try:
        settings = load_settings()
    except ConfigError as exc:
        raise HTTPException(status_code=503, detail=f"Config error: {exc}") from exc

    try:
        answer = ask(request.question, settings)
    except Exception as exc:
        logger.exception("Agent invocation failed")
        raise HTTPException(status_code=502, detail="Agent failed to answer") from exc

    elapsed = time.monotonic() - started
    logger.info("answered in %.2fs: %s", elapsed, request.question[:80])

    return AskResponse(
        question=request.question,
        answer=answer,
        elapsed_seconds=round(elapsed, 2),
    )
