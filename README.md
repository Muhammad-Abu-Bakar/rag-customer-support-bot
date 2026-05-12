# 🤖 AI Customer Support Bot with RAG

> Retrieval-augmented Telegram bot that answers questions about Stripe webhooks documentation in real time, with citations back to source.

**[👉 Try the live bot on Telegram](https://t.me/abubakar_rag_bot)**

![Demo](./screenshots/hero-telegram-demo.png)

---

## Why this project?

Most AI Automation Engineer / n8n Developer job listings ask for **RAG, vector databases, and AI agents** — but few public n8n projects demonstrate all three end-to-end. This bot ingests Stripe's webhook docs into a vector database, then uses a Telegram-hosted AI agent to answer developer questions with citations linking back to the source pages.

Built in a weekend. Live for anyone to test.

## What it does

1. **Ingest** — Pulls Stripe webhook docs via Jina Reader, chunks at 800 tokens with 100 overlap, embeds with OpenAI's `text-embedding-3-small` (1536 dims), and upserts to Pinecone with rich metadata (`source_title`, `source_url`, `doc_type`).
2. **Retrieve** — On every Telegram message, an n8n AI Agent (GPT-4o-mini) calls a Pinecone retrieval tool, gets the top 4 most similar chunks, and grounds its answer in them.
3. **Reply with citations** — Every answer ends with a `*Sources:*` section listing the docs used, as clickable links in Telegram.

## Demo

| You ask | Bot replies |
|---|---|
| _"How do I verify a Stripe webhook signature?"_ | Step-by-step answer + clickable citations to the signatures and quickstart docs |
| _"What happens if my server is down when a webhook fires?"_ | Explanation of retry behavior + citations to the undelivered events doc |
| _"What's the best biryani recipe?"_ | Honest fallback: _"I don't have enough information in the Stripe webhooks knowledge base..."_ |

## Architecture

​```mermaid
graph TB
    subgraph Ingestion["Ingestion · run manually"]
        I1[Docs URLs] -->|Jina Reader| I2[Markdown]
        I2 -->|Chunk 800/100| I3[Chunks + metadata]
        I3 -->|text-embedding-3-small| I4[1536-dim vectors]
        I4 --> P[(Pinecone<br/>saas-docs index)]
    end

    subgraph Bot["Bot · active 24/7"]
        U[User on Telegram] --> T[Telegram Trigger]
        T --> A[AI Agent · gpt-4o-mini]
        A <-->|retrieve top-4| P
        A --> S[Send reply with citations]
        S --> U
    end
​```

## Stack

| Layer | Tool | Why |
|---|---|---|
| Orchestration | **n8n** | Visual workflow builder, native AI Agent + Vector Store nodes |
| Vector database | **Pinecone** | Serverless free tier, strongest job-listing keyword for RAG roles |
| Embeddings | **OpenAI text-embedding-3-small** | 1536 dims, $0.02/1M tokens |
| LLM | **OpenAI GPT-4o-mini** | Cheap, low temperature (0.2) for grounded answers |
| Doc fetcher | **Jina Reader** | Free, converts any URL to clean markdown |
| Bot interface | **Telegram Bot API** | 5-minute setup, native n8n trigger |

Hosted on **n8n Cloud**. See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for full decision rationale.

## Numbers

- **7 docs** ingested from `docs.stripe.com/webhooks`
- **171 chunks** in Pinecone, ~24 chunks per doc
- **5–10s** average response time (message → reply)
- **~405 tokens** per AI Agent invocation (cost: ~$0.0002 per question)
- **Free tier all the way** — Pinecone Starter, Telegram, n8n Cloud Starter

## Lessons learned

Three insights from this build that I'd bring to a production system:

**1. Metadata matters more than retrieval tuning.**
Spending 30 minutes designing the chunk metadata schema (`source_title`, `source_url`, `doc_type`, `ingested_at`) paid off massively — those fields drive the citation feature and let the agent give answers users can verify. Most RAG demos skip this and end up with unverifiable outputs.

**2. n8n's `=` expression syntax has a UI gotcha.**
The first ingestion run wrote `=Stripe — Webhooks Overview` (literal `=` prefix) into every metadata field because I typed expressions as `={{ ... }}` instead of just `{{ ... }}`. Easy fix once spotted — the leading `=` is a mode toggle, not a character you type. Worth knowing.

**3. RAG systems fail on the input side, not just the output side.**
During testing, a vulgar message that happened to contain the keyword "webhook" got a perfectly-grounded answer about Stripe webhook setup. The retrieval worked. The LLM didn't hallucinate. But the input was garbage. In production I'd add OpenAI's Moderation API or a small content classifier in front of the agent — RAG needs guardrails on inputs, not just outputs.

## Repo structure

​```
.
├── workflows/                 # exported n8n workflow JSON
│   ├── 01-ingestion.json
│   └── 02-bot.json
├── samples/
│   └── stripe-webhooks-dataset.md   # what was ingested + stats
├── screenshots/               # workflow canvas + demo screenshots
├── docs/
│   ├── ARCHITECTURE.md
│   └── SETUP.md
└── README.md
​```

## Reproduce this

See [`docs/SETUP.md`](docs/SETUP.md) for full setup — Pinecone config, n8n credentials, Telegram bot creation, and step-by-step build instructions.

## Roadmap

Things I'd add for v2:

- **Web chat widget** mounted on a static site (more authentic for SaaS docs than Telegram)
- **Multi-tenant namespacing** — one Pinecone namespace per ingested SaaS company
- **Auto-crawl + scheduled re-ingest** when docs update
- **Content moderation** on user input (OpenAI Moderation API)
- **Re-ranking** with a cross-encoder for higher-precision retrieval
- **Chat memory** for multi-turn conversations
- **Eval suite** with golden Q&A pairs and faithfulness scoring

## Author

Built by **Muhammad Abubakar** — n8n / AI Automation Engineer based in Lahore.

- GitHub: [@Muhammad-Abu-Bakar](https://github.com/Muhammad-Abu-Bakar)
- Try the live bot: [@abubakar_rag_bot on Telegram](https://t.me/abubakar_rag_bot)
- Other projects: [ASO Analyzer](https://github.com/Muhammad-Abu-Bakar/aso-analyzer)

---

_MIT License · Built in n8n, May 2026._
