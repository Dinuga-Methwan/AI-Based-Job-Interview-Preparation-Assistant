import pytest
from ai.nlp_processor import get_embedding

def test_embedding_dimension_is_384():
    """Sanity check: the embedding model must produce 384‑dim vectors.
    This catches accidental use of a different SentenceTransformer model.
    """
    emb = get_embedding("test")
    # get_embedding returns a NumPy array; check its first dimension length
    assert hasattr(emb, "shape"), "Embedding should be a NumPy array"
    assert emb.shape[0] == 384, f"Expected embedding dimension 384, got {emb.shape[0]}"
