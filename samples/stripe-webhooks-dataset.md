# Demo Dataset: Stripe Webhooks Docs

v1 RAG corpus built from Stripe's public webhooks documentation.

## URLs ingested
| Title | URL | doc_type |
|---|---|---|
| Stripe — Webhooks Overview | https://docs.stripe.com/webhooks | overview |
| Stripe — Webhook Builder (Quickstart) | https://docs.stripe.com/webhooks/quickstart | tutorial |
| Stripe — Handling Payment Events | https://docs.stripe.com/webhooks/handling-payment-events | tutorial |
| Stripe — Webhook Versioning | https://docs.stripe.com/webhooks/versioning | tutorial |
| Stripe — Resolve Signature Verification Errors | https://docs.stripe.com/webhooks/signature | troubleshooting |
| Stripe — Process Undelivered Events | https://docs.stripe.com/webhooks/process-undelivered-events | tutorial |
| Stripe — Event Destinations Overview | https://docs.stripe.com/event-destinations | overview |

## Stats
- Pinecone namespace: `stripe-webhooks-v1`
- Total chunks: 171
- Chunk size: 800 tokens, 100 overlap
- Embedding model: `text-embedding-3-small` (1536 dims)
- Ingestion date: 2026-05-11

## Why Stripe Webhooks?
Focused topic, recognizable brand, rich enough for non-trivial retrieval demos.

## Sample questions the bot should handle well
- "How do I verify a Stripe webhook signature?"
- "How should I handle a successful payment event?"
- "What happens if my server is down when a webhook fires?"
- "How do I migrate my webhook to a new API version?"
- "Why is my webhook signature verification failing?"
- "How do I test webhooks before going live?"
