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
    # Normalize query embedding
    query_norm = query_embedding / (np.linalg.norm(query_embedding) + 1e-8)
    # Normalize document embeddings
    doc_norms = doc_embeddings / (np.linalg.norm(doc_embeddings, axis=1, keepdims=True) + 1e-8)
    # Compute dot product (cosine similarity)
    similarities = np.dot(doc_norms, query_norm)
    return similarities


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

    # Embed the query
    query_embedding = embed_texts([query])[0]  # shape: (embedding_dim,)
    # Compute similarity scores
    scores = cosine_similarity(query_embedding, doc_embeddings)
    # Get indices of top_k scores
    top_indices = np.argsort(scores)[-top_k:][::-1]
    # Return the top_k most relevant documents
    return [documents[i] for i in top_indices]
