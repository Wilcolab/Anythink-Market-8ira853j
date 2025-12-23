from dataclasses import dataclass
from typing import Literal


@dataclass
class RAGConfig:
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o-mini"
    top_k: int = 3
    retrieval_strategy: Literal["cosine", "euclidean"] = "cosine"
    max_context_length: int = 4000


config = RAGConfig()

