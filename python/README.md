# RAG Support Bot — Python / LangChain

Production-oriented reimplementation of the n8n RAG bot in Python using
LangChain 1.x, FastAPI, and Pinecone.

**Why two implementations?** The n8n version (see repo root) was built for
speed of iteration and visual debuggability. This version exists for the
things n8n makes awkward: version-controlled logic, unit tests, evals,
and deployment as a REST service a client's app can call directly.

## Stack
- LangChain 1.x (`create_agent` + middleware)
- OpenAI `text-embedding-3-small` (1536-dim) + `gpt-4o-mini`
- Pinecone serverless (cosine)
- FastAPI
- LangSmith for tracing and evals

## Status
Step 1 of 7 — scaffold complete.

## Setup
    cd python
    uv venv --python 3.12
    source .venv/bin/activate
    uv pip install -e ".[api,dev]"
    cp .env.example .env

Then fill in real keys in `.env`.

## Layout
- `src/rag_bot/` — package code (config, ingestion, retrieval, agent, api)
- `scripts/` — one-off runnable scripts (ingest, query)
- `tests/` — unit tests
- `evals/` — question/expected-answer pairs for regression testing
