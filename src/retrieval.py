import numpy as np
from src.config import config
from src.embeddings import embed_texts


def cosine_similarity(query_embedding: np.ndarray, doc_embeddings: np.ndarray) -> np.ndarray:
    """
    Compute cosine similarity between query and all document embeddings.
    
    TODO: Implement this function
    - Normalize the query embedding
    - Normalize the document embeddings
    - Compute dot product between normalized query and all documents
    - Return array of similarity scores
    """
    raise NotImplementedError("Implement cosine_similarity function")


def retrieve(
    query: str,
    documents: list[dict],
    doc_embeddings: np.ndarray,
    top_k: int | None = None
) -> list[dict]:
    """
    Retrieve the most relevant documents for a query.
    
    TODO: Implement this function
    - Embed the query using embed_texts
    - Compute similarity scores between query and all documents
    - Return the top_k most similar documents
    
    Args:
        query: The search query string
        documents: List of document dictionaries
        doc_embeddings: Pre-computed embeddings for all documents
        top_k: Number of documents to retrieve (defaults to config.top_k)
    
    Returns:
        List of the top_k most relevant documents
    """
    if top_k is None:
        top_k = config.top_k
    
    raise NotImplementedError("Implement retrieve function")
