"""
MedIntel AI - FAISS Vector Store
"""
import os
import pickle
from typing import List, Dict, Tuple, Optional
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.config import VECTOR_DIR, EMBEDDING_MODEL

# Try to import required libraries
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

# Global variables for model and index
_embedding_model = None
_faiss_index = None
_document_store = []  # List of (chunk_text, metadata) tuples

INDEX_PATH = VECTOR_DIR / "faiss_index.bin"
STORE_PATH = VECTOR_DIR / "document_store.pkl"


def get_embedding_model():
    """Get or initialize embedding model."""
    global _embedding_model
    
    if not TRANSFORMERS_AVAILABLE:
        return None
    
    if _embedding_model is None:
        try:
            _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            return None
    
    return _embedding_model


def create_embeddings(texts: List[str]) -> Optional[np.ndarray]:
    """
    Create embeddings for a list of texts.
    
    Args:
        texts: List of text strings
        
    Returns:
        Numpy array of embeddings
    """
    model = get_embedding_model()
    if model is None:
        return None
    
    try:
        embeddings = model.encode(texts, show_progress_bar=False)
        return np.array(embeddings).astype('float32')
    except Exception as e:
        print(f"Error creating embeddings: {e}")
        return None


def create_single_embedding(text: str) -> Optional[np.ndarray]:
    """
    Create embedding for a single text.
    
    Args:
        text: Text string
        
    Returns:
        Numpy array of embedding
    """
    embeddings = create_embeddings([text])
    if embeddings is not None:
        return embeddings[0]
    return None


def create_or_load_faiss_index(dimension: int = 384) -> bool:
    """
    Create or load FAISS index.
    
    Args:
        dimension: Embedding dimension (384 for all-MiniLM-L6-v2)
        
    Returns:
        True if successful
    """
    global _faiss_index, _document_store
    
    if not FAISS_AVAILABLE:
        print("FAISS not available")
        return False
    
    # Try to load existing index
    if INDEX_PATH.exists() and STORE_PATH.exists():
        try:
            _faiss_index = faiss.read_index(str(INDEX_PATH))
            with open(STORE_PATH, 'rb') as f:
                _document_store = pickle.load(f)
            return True
        except Exception as e:
            print(f"Error loading index: {e}")
    
    # Create new index
    try:
        _faiss_index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        _document_store = []
        return True
    except Exception as e:
        print(f"Error creating index: {e}")
        return False


def add_document_chunks(chunks: List[Dict]) -> bool:
    """
    Add document chunks to vector store.
    
    Args:
        chunks: List of chunk dictionaries with 'text' and metadata
        
    Returns:
        True if successful
    """
    global _faiss_index, _document_store
    
    if _faiss_index is None:
        if not create_or_load_faiss_index():
            return False
    
    if not chunks:
        return True
    
    # Extract texts
    texts = [chunk['text'] for chunk in chunks]
    
    # Create embeddings
    embeddings = create_embeddings(texts)
    if embeddings is None:
        return False
    
    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)
    
    # Add to index
    try:
        _faiss_index.add(embeddings)
        
        # Store chunks with metadata
        for chunk in chunks:
            _document_store.append(chunk)
        
        # Save index and store
        save_index()
        return True
    
    except Exception as e:
        print(f"Error adding to index: {e}")
        return False


def search_similar_chunks(query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
    """
    Search for similar chunks.
    
    Args:
        query: Search query
        top_k: Number of results to return
        
    Returns:
        List of (chunk_dict, score) tuples
    """
    global _faiss_index, _document_store
    
    if _faiss_index is None:
        if not create_or_load_faiss_index():
            return []
    
    if _faiss_index.ntotal == 0:
        return []
    
    # Create query embedding
    query_embedding = create_single_embedding(query)
    if query_embedding is None:
        return []
    
    # Normalize for cosine similarity
    query_embedding = query_embedding.reshape(1, -1).astype('float32')
    faiss.normalize_L2(query_embedding)
    
    # Search
    try:
        k = min(top_k, _faiss_index.ntotal)
        scores, indices = _faiss_index.search(query_embedding, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx >= 0 and idx < len(_document_store):
                results.append((_document_store[idx], float(scores[0][i])))
        
        return results
    
    except Exception as e:
        print(f"Error searching index: {e}")
        return []


def save_index():
    """Save FAISS index and document store to disk."""
    global _faiss_index, _document_store
    
    if _faiss_index is None:
        return
    
    try:
        faiss.write_index(_faiss_index, str(INDEX_PATH))
        with open(STORE_PATH, 'wb') as f:
            pickle.dump(_document_store, f)
    except Exception as e:
        print(f"Error saving index: {e}")


def load_index() -> bool:
    """Load FAISS index and document store from disk."""
    return create_or_load_faiss_index()


def clear_index():
    """Clear the vector store."""
    global _faiss_index, _document_store
    
    _faiss_index = None
    _document_store = []
    
    # Delete files
    if INDEX_PATH.exists():
        INDEX_PATH.unlink()
    if STORE_PATH.exists():
        STORE_PATH.unlink()
    
    # Create fresh index
    create_or_load_faiss_index()


def get_index_stats() -> Dict:
    """Get statistics about the vector store."""
    global _faiss_index, _document_store
    
    if _faiss_index is None:
        create_or_load_faiss_index()
    
    return {
        'total_chunks': _faiss_index.ntotal if _faiss_index else 0,
        'document_store_size': len(_document_store),
        'index_trained': _faiss_index.is_trained if _faiss_index else False,
        'embedding_dimension': _faiss_index.d if _faiss_index else 0
    }


def check_vector_store_available() -> bool:
    """Check if vector store is available."""
    return FAISS_AVAILABLE and TRANSFORMERS_AVAILABLE


def get_all_documents_in_store() -> List[str]:
    """Get list of unique document names in store."""
    global _document_store
    
    if not _document_store:
        load_index()
    
    doc_names = set()
    for chunk in _document_store:
        if 'document_name' in chunk:
            doc_names.add(chunk['document_name'])
    
    return list(doc_names)


def delete_document_from_store(document_name: str) -> bool:
    """
    Remove all chunks for a document from the store.
    Note: This requires rebuilding the FAISS index.
    
    Args:
        document_name: Name of document to remove
        
    Returns:
        True if successful
    """
    global _faiss_index, _document_store
    
    if not _document_store:
        return True
    
    # Filter out chunks from this document
    remaining_chunks = [
        chunk for chunk in _document_store 
        if chunk.get('document_name') != document_name
    ]
    
    if len(remaining_chunks) == len(_document_store):
        # Document not found
        return True
    
    # Rebuild index with remaining chunks
    clear_index()
    
    if remaining_chunks:
        return add_document_chunks(remaining_chunks)
    
    return True
