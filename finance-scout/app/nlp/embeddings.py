from __future__ import annotations

import hashlib

import numpy as np


def embed_text(text: str, dim: int = 128) -> np.ndarray:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    data = np.frombuffer(digest, dtype=np.uint8)
    repeats = (dim // len(data)) + 1
    vector = np.tile(data, repeats)[:dim]
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector.astype(float)
    return (vector / norm).astype(float)


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    denom = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if denom == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / denom)
