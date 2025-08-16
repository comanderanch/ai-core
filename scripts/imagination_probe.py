#!/usr/bin/env python3
import json, time, hashlib
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BUF_DIR = BASE / "memory" / "imagination"
BUF_FILE = BUF_DIR / "imagination_buffer.jsonl"
MODEL = BASE / "memory" / "ngram" / "bigram_model.json"

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def try_bigram(prompt: str) -> tuple[str,str]:
    try:
        from scripts.ngram_reply_engine import load_model, generate_reply
        if MODEL.exists():
            m = load_model(str(MODEL))
            return generate_reply(m, prompt, max_len=120), "imagination_probe.py:bigram"
    except Exception:
        pass
    # safe fallback (no learning, no memory writes)
    return (prompt[::-1] if prompt else ""), "imagination_probe.py:fallback"
    
def main():
    BUF_DIR.mkdir(parents=True, exist_ok=True)
    prompt = input("imagination> ").strip()
    draft, prov = try_bigram(prompt)
    rec = {
        "ts": time.time(),
        "prompt": prompt,
        "draft": draft,
        "prompt_sha256": sha256(prompt),
        "draft_sha256": sha256(draft),
        "provenance": prov,
        "q_state": "isolated"
    }
    with BUF_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"[OK] wrote {BUF_FILE}")

if __name__ == "__main__":
    main()
