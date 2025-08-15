# tools/remap_training_freqs_to_palette.py
#!/usr/bin/env python3
import csv, math
from pathlib import Path

TRAIN_IN  = Path("training/training_set.csv")
TRAIN_OUT = Path("training/training_set_remapped.csv")
PAL       = Path("tokenizer/full_color_tokens.csv")
EPS       = 1.0  # accept nearest palette freq within 1.0

def load_palette_freqs(p: Path):
    freqs = set()
    with p.open("r", encoding="utf-8", newline="") as f:
        rdr = csv.reader(f)
        header = next(rdr, None)
        for row in rdr:
            if not row: continue
            if len(row) >= 10:
                try: freqs.add(float(row[9]))
                except: pass
            elif len(row) >= 6:
                try: freqs.add(float(row[5]))
                except: pass
    return sorted(freqs)

def nearest(v, arr):
    best = None; bd = 1e18
    for x in arr:
        d = abs(x - v)
        if d < bd:
            bd = d; best = x
    return best, bd

def main():
    pal_freqs = load_palette_freqs(PAL)
    if not pal_freqs:
        raise SystemExit("[ERR] no palette freqs")
    with TRAIN_IN.open("r", encoding="utf-8", newline="") as fi, \
         TRAIN_OUT.open("w", encoding="utf-8", newline="") as fo:
        rdr = csv.DictReader(fi)
        fw  = csv.DictWriter(fo, fieldnames=rdr.fieldnames)
        fw.writeheader()
        fixed = skipped = total = 0
        for row in rdr:
            total += 1
            lab = row["label"].strip().strip('"')
            parts = lab.split(",")
            if len(parts) != 4:
                skipped += 1
                fw.writerow(row); continue
            try:
                r,g,b = map(lambda x: int(float(x)), parts[:3])
                f     = float(parts[3])
            except:
                skipped += 1
                fw.writerow(row); continue
            # snap frequency
            nf, d = nearest(f, pal_freqs)
            if d <= EPS and nf is not None:
                parts[3] = f"{nf}"
                row["label"] = ",".join(map(str, parts))
                fixed += 1
            fw.writerow(row)
    print(f"[OK] wrote {TRAIN_OUT} | total={total} fixed={fixed} skipped={skipped}")

if __name__ == "__main__":
    main()
