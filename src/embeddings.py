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
    raise NotImplementedError("Implement embed_texts function")


def embed_documents(documents: list[dict]) -> tuple[list[dict], np.ndarray]:
    """
    Embed all documents and return both documents and their embeddings.
    
    TODO: Implement this function
    - Extract text content from each document (combine title and content)
    - Generate embeddings for all documents
    - Return tuple of (documents list, embeddings array)
    """
    raise NotImplementedError("Implement embed_documents function")
