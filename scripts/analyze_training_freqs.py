# scripts/analyze_training_freqs.py
#!/usr/bin/env python3
import csv, collections
from pathlib import Path

TRAIN = Path("training/training_set.csv")

def main():
    c = collections.Counter()
    with TRAIN.open("r", encoding="utf-8", newline="") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            lab = row["label"].strip().strip('"')
            parts = lab.split(",")
            if len(parts) != 4: continue
            c[parts[3]] += 1
    for k, v in c.most_common():
        print(f"{k}\t{v}")
if __name__ == "__main__":
    main()
