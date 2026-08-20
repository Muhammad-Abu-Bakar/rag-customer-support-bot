"""The support agent: Claude + a retrieval tool, answering only from the corpus."""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from rag_bot.config import Settings, load_settings
from rag_bot.retrieval import retrieve

SYSTEM_PROMPT = """You are a customer support assistant for Stripe's webhooks documentation.

RULES:
1. Always call `search_docs` before answering any question about Stripe, webhooks,
   or the product. Never answer from your own knowledge.
2. Ground every factual claim in the retrieved chunks. If the chunks don't contain
   the answer, say so plainly: "I don't have that in my documentation." Do not
   guess or fill gaps from general knowledge.
3. End every answer with a Sources section listing the markdown links returned by
   the tool. Only cite sources you actually used.
4. If the question is not about Stripe webhooks, decline briefly and say what you
   can help with. Do not answer off-topic questions even if you know the answer.
5. Keep answers concise. Prefer the documentation's own terminology.
"""


def _format_chunks(chunks) -> str:
    """Render retrieved chunks for the model, one block per chunk."""
    if not chunks:
        return "No relevant documentation found."

    blocks = []
    for i, c in enumerate(chunks, start=1):
        blocks.append(
            f"[Chunk {i}] (relevance {c.score:.3f})\n"
            f"Source: {c.citation}\n\n"
            f"{c.text}"
        )
    return "\n\n---\n\n".join(blocks)


def build_agent(settings: Settings | None = None):
    """Build the agent. Settings are captured in the tool's closure."""
    settings = settings or load_settings()

    @tool
    def search_docs(query: str) -> str:
        """Search the Stripe webhooks documentation.

        Use this for any question about webhooks, endpoints, signatures, events,
        or Stripe behaviour. Returns relevant documentation chunks with their
        sources. Pass a focused search phrase, not the user's whole message.
        """
        chunks = retrieve(settings, query)
        return _format_chunks(chunks)

    model = ChatOpenAI(
        model=settings.chat_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )

    return create_agent(
        model=model,
        tools=[search_docs],
        system_prompt=SYSTEM_PROMPT,
    )


def ask(question: str, settings: Settings | None = None) -> str:
    """Ask a single question and return the final answer text."""
    agent = build_agent(settings)
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].content
