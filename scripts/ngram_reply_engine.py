#!/usr/bin/env python3
# Minimal bigram engine over training_data/*.txt
import re, json, random
from pathlib import Path
from collections import defaultdict, Counter

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")

def tokenize_text(text: str):
    return [m.group(0).lower() for m in WORD_RE.finditer(text)]

def build_bigram_model(text_dir: Path):
    next_counts = defaultdict(Counter)   # prev -> Counter(next)
    files = sorted(text_dir.glob("*.txt"))
    total_tokens = 0
    for fp in files:
        text = fp.read_text(encoding="utf-8", errors="ignore")
        words = tokenize_text(text)
        total_tokens += len(words)
        for a, b in zip(words, words[1:]):
            next_counts[a][b] += 1
    # Sorted next-word lists for stable iteration
    next_sorted = {w: [x for x,_ in c.most_common()] for w,c in next_counts.items()}
    return {"next_sorted": next_sorted, "total_tokens": total_tokens, "files": [f.name for f in files]}

def save_model(model, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(model, ensure_ascii=False))

def load_model(path: Path):
    return json.loads(path.read_text())

def generate_reply(prompt: str, model, max_len=16, k=3):
    """
    Bigram reply with top-K sampling (default K=3), randomness seeded by prompt
    so the same prompt gives the same reply, different prompts vary.
    """
    ns = model.get("next_sorted", {})
    words = tokenize_text(prompt)
    out = []

    # seed RNG from prompt for deterministic variety
    random.seed(hash(prompt) & 0xffffffff)

    # choose seed
    seed = words[-1] if words else None
    if seed not in ns:
        for k0 in sorted(ns.keys()):
            seed = k0
            break
    if seed is None:
        return ""  # corpus empty

    curr = seed
    for _ in range(max_len):
        out.append(curr)
        nxts = ns.get(curr)
        if not nxts:
            break
        pool = nxts[:k] if len(nxts) >= k else nxts
        curr = random.choice(pool)
    return " ".join(out)
