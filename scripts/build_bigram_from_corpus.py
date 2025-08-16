#!/usr/bin/env python3
import json, argparse, re
from collections import defaultdict, Counter

WORD = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")

def toks(s): 
    return [m.group(0).lower() for m in WORD.finditer(s)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="outp", required=True)
    args = ap.parse_args()

    with open(args.inp, "r", encoding="utf-8") as f:
        text = f.read()

    tokens = toks(text)
    bigrams = defaultdict(Counter)
    for a, b in zip(tokens, tokens[1:]):
        bigrams[a][b] += 1

    model = {
        w: {n: c / sum(cnt.values()) for n, c in cnt.items()}
        for w, cnt in bigrams.items()
    }
    with open(args.outp, "w", encoding="utf-8") as f:
        json.dump({"type": "bigram", "model": model}, f, ensure_ascii=False)
    print(f"[✓] wrote {args.outp} ({len(model)} states)")
if __name__ == "__main__":
    main()
