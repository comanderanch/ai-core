import csv
from pathlib import Path

# Settings
SOURCE_FILE = Path("tokenizer/full_color_tokens.csv")
TARGET_FILE = Path("training/training_set.csv")
ROWS_TO_LOAD = 10  # Change this for more

def generate_training_set():
    if not SOURCE_FILE.exists():
        print(f"[✗] Source file not found: {SOURCE_FILE}")
        return

    output_rows = []

    with SOURCE_FILE.open("r") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i >= ROWS_TO_LOAD:
                break

            try:
                r = float(row[-4])
                g = float(row[-3])
                b = float(row[-2])

                input_token = r + g
                target_token = b
                label = f"{int(r)},{int(g)},{int(b)}"
                weight = 1.0

                output_rows.append([input_token, target_token, label, weight])

            except (ValueError, IndexError):
                continue  # Skip malformed rows

    # Write output CSV
    with TARGET_FILE.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["input_token", "target_token", "label", "weight"])
        writer.writerows(output_rows)

    print(f"[✓] Wrote {len(output_rows)} token pairs to {TARGET_FILE}")

if __name__ == "__main__":
    generate_training_set()
