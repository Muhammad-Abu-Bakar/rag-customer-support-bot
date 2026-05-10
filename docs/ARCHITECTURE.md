# Architecture

## Stack decisions

| Layer | Choice | Why |
|---|---|---|
| Vector DB | Pinecone (Starter tier) | Strongest job-listing keyword, native n8n node, fastest setup |
| Embeddings | OpenAI `text-embedding-3-small` | $0.02/1M tokens, 1536 dims, native node |
| LLM | OpenAI `gpt-4o-mini` | Cheap, capable, consistent with portfolio |
| Orchestration | n8n AI Agent + Pinecone Vector Store as tool | Earns the "AI agent" keyword |
| Bot interface (v1) | Telegram | 5-minute setup, free, easy demo |
| Bot interface (v1.5) | Web widget on static page → n8n webhook | Authentic to SaaS support niche |

## Chunking strategy
- **Splitter:** Recursive Character Text Splitter (n8n native)
- **Chunk size:** 800 tokens (~600 words)
- **Overlap:** 100 tokens (~12%)
- **Metadata per chunk:**
  - `source_doc` — filename or URL
  - `source_title` — human-readable title
  - `source_url` — deep link
  - `chunk_index` — position within doc
  - `doc_type` — api_reference / tutorial / faq / changelog
  - `ingested_at` — ISO timestamp

## Data flow
**Ingestion:** Manual Trigger → Read File → Default Data Loader →
Recursive Text Splitter → Embeddings (OpenAI) → Pinecone Vector Store (Insert)

**Bot:** Telegram Trigger → AI Agent
    ├── Chat Model: OpenAI gpt-4o-mini
    └── Tool: Pinecone Vector Store (Retrieve, top-k=4)
→ Telegram Send Message

## Out of scope for v1
Web widget, multi-tenant namespacing, auto-crawler, chat memory, re-ranking.
