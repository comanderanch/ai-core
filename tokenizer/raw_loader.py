# tokenizer/raw_loader.py
# Minimal RAW RGB loader for ai-core (facts only, deterministic)

import hashlib
from typing import List, Tuple

def load_raw_rgb(path: str) -> bytes:
    """Read raw RGB bytes. Length must be divisible by 3."""
    data = open(path, "rb").read()
    if len(data) % 3 != 0:
        raise ValueError(f"{path}: size {len(data)} not divisible by 3")
    return data

def count_colors(raw: bytes) -> int:
    """Number of RGB triplets."""
    return len(raw) // 3

def sha256_bytes(raw: bytes) -> str:
    """SHA256 of the byte buffer (hex)."""
    return hashlib.sha256(raw).hexdigest()

def as_triplets(raw: bytes) -> List[Tuple[int,int,int]]:
    """Return a list of (r,g,b) triplets (0..255)."""
    it = iter(raw)
    return list(zip(it, it, it))
