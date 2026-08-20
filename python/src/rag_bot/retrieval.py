"""Vector store access.

Wraps the existing Pinecone index in a LangChain VectorStore so the rest of the
package can retrieve documents without knowing about Pinecone specifically.
"""

from dataclasses import dataclass

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

from rag_bot.config import Settings

# The metadata key holding chunk text in the existing index.
TEXT_KEY = "text"


def build_vector_store(settings: Settings) -> PineconeVectorStore:
    """Connect to the existing index. Does not create or modify anything."""
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )
    pc = Pinecone(api_key=settings.pinecone_api_key)
    index = pc.Index(settings.pinecone_index_name)

    return PineconeVectorStore(
        index=index,
        embedding=embeddings,
        namespace=settings.pinecone_namespace,
        text_key=TEXT_KEY,
    )


@dataclass(frozen=True)
class RetrievedChunk:
    """A retrieved chunk plus the fields needed to cite it."""

    text: str
    score: float
    source_title: str
    source_url: str
    doc_type: str

    @classmethod
    def from_document(cls, doc: Document, score: float) -> "RetrievedChunk":
        md = doc.metadata or {}
        return cls(
            text=doc.page_content,
            score=score,
            source_title=md.get("source_title", "Unknown source"),
            source_url=md.get("source_url", ""),
            doc_type=md.get("doc_type", ""),
        )

    @property
    def citation(self) -> str:
        return f"[{self.source_title}]({self.source_url})" if self.source_url else self.source_title


def retrieve(settings: Settings, question: str, k: int | None = None) -> list[RetrievedChunk]:
    """Embed the question and return the k most similar chunks, best first."""
    store = build_vector_store(settings)
    results = store.similarity_search_with_score(question, k=k or settings.top_k)
    return [RetrievedChunk.from_document(doc, score) for doc, score in results]
