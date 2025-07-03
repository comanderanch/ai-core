# training/training_loader.py

import csv

def load_training_data(csv_path="training_set.csv"):
    training_data = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    input_token = int(row['input_token'])
                    target_token = int(row['target_token'])
                    label = row['label']
                    weight = float(row['weight'])
                    training_data.append((input_token, target_token, label, weight))
                except (ValueError, KeyError) as e:
                    print(f"[WARN] Skipping malformed row: {row} — {e}")
    except FileNotFoundError:
        print(f"[ERROR] File '{csv_path}' not found.")
    return training_data
