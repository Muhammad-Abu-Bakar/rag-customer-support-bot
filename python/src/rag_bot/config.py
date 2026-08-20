"""Central configuration. Everything tunable lives here, loaded from the environment.

Nothing else in the package should read os.environ directly.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_ENV_PATH)


class ConfigError(RuntimeError):
    """Raised when a required setting is missing or malformed."""


def _require(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value or value.endswith("..."):
        raise ConfigError(
            f"{name} is missing or still a placeholder in {_ENV_PATH}. "
            f"Set a real value and try again."
        )
    return value


def _optional(name: str, default: str) -> str:
    return os.getenv(name, "").strip() or default


def _int(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ConfigError(f"{name} must be an integer, got {raw!r}") from exc


@dataclass(frozen=True)
class Settings:
    pinecone_api_key: str
    pinecone_index_name: str
    pinecone_namespace: str

    embedding_model: str
    chat_model: str

    chunk_size: int
    chunk_overlap: int
    top_k: int

    @property
    def openai_api_key(self) -> str:
        """Only needed for embedding. Resolved lazily so Pinecone-only work
        doesn't fail when the key is absent."""
        return _require("OPENAI_API_KEY")

    @property
    def anthropic_api_key(self) -> str:
        """Only needed for generation. Resolved lazily for the same reason."""
        return _require("ANTHROPIC_API_KEY")


def load_settings() -> Settings:
    return Settings(
        pinecone_api_key=_require("PINECONE_API_KEY"),
        pinecone_index_name=_require("PINECONE_INDEX_NAME"),
        pinecone_namespace=_require("PINECONE_NAMESPACE"),
        embedding_model=_optional("EMBEDDING_MODEL", "text-embedding-3-small"),
        chat_model=_optional("CHAT_MODEL", "claude-haiku-4-5-20251001"),
        chunk_size=_int("CHUNK_SIZE", 800),
        chunk_overlap=_int("CHUNK_OVERLAP", 100),
        top_k=_int("TOP_K", 4),
    )
