#!/usr/bin/env python3
import csv, json, re, subprocess, sys
from pathlib import Path
from typing import List, Tuple, Dict

# Resolve repo root from this file path
BASE_DIR = Path(__file__).resolve().parent.parent
PALETTE_CSV = BASE_DIR / "tokenizer" / "full_color_tokens.csv"
TEXT_DIR    = BASE_DIR / "training_data"
OUT_CSV     = BASE_DIR / "training" / "training_set_text_tokens.csv"
MAP_JSON    = BASE_DIR / "training_data" / "word_to_token_map.json"

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")

def load_palette_rows(p: Path) -> List[Tuple[str,float,int,int,int,float]]:
    """
    Return list of rows in palette order:
      (token_str, hue_bin_or_val, R, G, B, Freq)
    Supports 6-col or 10-col rows.
    """
    rows = []
    with p.open("r", encoding="utf-8", newline="") as f:
        rdr = csv.reader(f)
        header = next(rdr, None)
        for r in rdr:
            if not r: continue
            c = [x.strip() for x in r]
            try:
                if len(c) >= 10:
                    token = c[0]
                    hue   = float(c[1]) if c[1] else 0.0
                    R     = int(float(c[6])); G = int(float(c[7])); B = int(float(c[8]))
                    F     = float(c[9])
                elif len(c) >= 6:
                    token = c[0]
                    hue   = float(c[1]) if c[1] else 0.0
                    R     = int(float(c[2])); G = int(float(c[3])); B = int(float(c[4]))
                    F     = float(c[5])
                else:
                    continue
                rows.append((token, hue, R, G, B, F))
            except Exception:
                continue
    if not rows:
        raise SystemExit(f"[ERR] No usable rows parsed from {p}")
    return rows

def collect_words(text_dir: Path) -> List[str]:
    vocab = []
    seen = set()
    files = sorted(text_dir.glob("*.txt"))
    if not files:
        raise SystemExit(f"[ERR] No .txt files found in {text_dir}")
    for fp in files:
        text = fp.read_text(encoding="utf-8", errors="ignore")
        for w in WORD_RE.findall(text):
            wl = w.lower()
            if wl not in seen:
                seen.add(wl); vocab.append(wl)
    return vocab

def build_word_to_token_map(words: List[str], palette: List[Tuple[str,float,int,int,int,float]]) -> Dict[str, int]:
    """
    Deterministic mapping by order:
      words[i] -> palette[i % len(palette)]
    Store mapping to *palette index* (0-based) for fast lookup.
    """
    M = len(palette)
    mapping = {}
    for i, w in enumerate(words):
        mapping[w] = i % M
    return mapping

def generate_training_pairs(words_seq: List[str],
                            w2i: Dict[str,int],
                            palette: List[Tuple[str,float,int,int,int,float]]) -> List[Tuple[float,float,str,float]]:
    """
    For consecutive words, emit (input_freq, target_freq, "R,G,B,Freq", 1.0)
    """
    pairs = []
    for i in range(len(words_seq)-1):
        w  = words_seq[i].lower()
        wn = words_seq[i+1].lower()
        if w not in w2i or wn not in w2i:  # should be rare
            continue
        i0 = w2i[w]; i1 = w2i[wn]
        _, _, R0, G0, B0, F0 = palette[i0]
        _, _, R1, G1, B1, F1 = palette[i1]
        # label uses the *target’s* color tuple (common in your existing CSV)
        label = f"{R1},{G1},{B1},{F1}"
        pairs.append((F0, F1, label, 1.0))
    return pairs

def stream_words_in_order(text_dir: Path) -> List[str]:
    """Concatenate all files in alpha order, preserving word order for sequence pairs."""
    seq = []
    for fp in sorted(text_dir.glob("*.txt")):
        text = fp.read_text(encoding="utf-8", errors="ignore")
        seq.extend([m.group(0).lower() for m in WORD_RE.finditer(text)])
    return seq

def main():
    if not PALETTE_CSV.exists():
        raise SystemExit(f"[ERR] Palette not found: {PALETTE_CSV}")
    palette = load_palette_rows(PALETTE_CSV)
    words   = collect_words(TEXT_DIR)
    w2i     = build_word_to_token_map(words, palette)

    # Save the mapping for interactive mode
    MAP_JSON.write_text(json.dumps({
        "palette_size": len(palette),
        "vocab_size": len(words),
        "word_to_palette_index": w2i
    }, ensure_ascii=False, indent=2))

    # Build the word sequence for training pairs
    word_seq = stream_words_in_order(TEXT_DIR)
    pairs = generate_training_pairs(word_seq, w2i, palette)

    # Write training CSV in your existing format
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["input_token","target_token","label","weight"])
        for F0, F1, label, w in pairs:
            wr.writerow([F0, F1, label, w])

    print(f"[OK] palette rows: {len(palette)}")
    print(f"[OK] vocab size:   {len(words)}")
    print(f"[OK] pairs written: {len(pairs)} → {OUT_CSV}")
    print(f"[OK] mapping saved: {MAP_JSON}")

    # Optional: kick the learning loop if present
    runner = BASE_DIR / "scripts" / "learning_loop_runner.py"
    if runner.exists():
        try:
            print("[i] launching learning loop…")
            subprocess.run(
                ["python3", str(runner), "--input", str(OUT_CSV)],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"[WARN] learning loop exited non-zero: {e}")
    else:
        print("[i] learning_loop_runner.py not found; skipping auto-train.")

if __name__ == "__main__":
    sys.exit(main())
