import numpy as np
from src.llm_client import get_embeddings
from src.config import config


def embed_texts(texts: list[str]) -> np.ndarray:
    """
    Convert a list of text strings into embeddings.
    
    TODO: Implement this function
    - Use the get_embeddings helper from llm_client
    - Use config.embedding_model for the model name
    - Return embeddings as a numpy array
    """
    # Use get_embeddings helper and config.embedding_model
    embeddings = get_embeddings(texts, model=config.embedding_model)
    return np.array(embeddings)


def embed_documents(documents: list[dict]) -> tuple[list[dict], np.ndarray]:
    """
    Embed all documents and return both documents and their embeddings.
    
    TODO: Implement this function
    - Extract text content from each document (combine title and content)
    - Generate embeddings for all documents
    - Return tuple of (documents list, embeddings array)
    """
    # Extract text content from each document (combine title and content)
    texts = []
    for doc in documents:
        # Combine title and content if both exist, else just content
        title = doc.get("title", "")
        content = doc.get("content", "")
        combined = f"{title} {content}".strip()
        texts.append(combined)
    embeddings = embed_texts(texts)
    return documents, embeddings
