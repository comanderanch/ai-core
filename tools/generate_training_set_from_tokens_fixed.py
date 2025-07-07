import csv
import numpy as np
from pathlib import Path

# === Paths ===
input_csv = Path("tokenizer/full_color_tokens.csv")
output_csv = Path("training/training_set.csv")

# === Load Token Data ===
tokens = []
with input_csv.open("r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            def parse(val):
                return int(val, 2) if all(c in "01" for c in val.strip()) else int(float(val))

            h = parse(row["Hue"])
            r = parse(row["Red"])
            g = parse(row["Green"])
            b = parse(row["Blue"])

            tokens.append({
                "vec": [h, r, g, b],
                "label": f"{h},{r},{g},{b}"
            })
        except Exception as e:
            print(f"[WARN] Skipping malformed row: {row} – {e}")

# === Generate Pairs ===
pairs = []
for i, a in enumerate(tokens):
    for j, b in enumerate(tokens):
        if i != j:
            pairs.append((a["vec"], b["vec"], b["label"]))

# === Save to Training CSV ===
with output_csv.open("w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["input_token", "target_token", "label", "weight"])
    for a_vec, b_vec, label in pairs:
        input_token = float(sum(a_vec))
        target_token = float(sum(b_vec))
        writer.writerow([input_token, target_token, label, 1.0])

print(f"[✓] Generated {len(pairs)} token pairs to {output_csv}")
