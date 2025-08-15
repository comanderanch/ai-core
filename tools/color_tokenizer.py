import csv
import hashlib

# Load full_color_tokens.csv once into memory
def load_color_token_map(csv_path='tokenizer/full_color_tokens.csv'):
    token_map = {}
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rgb_key = (int(row['Red']), int(row['Green']), int(row['Blue']))
            token_map[rgb_key] = row['Token']
    return token_map

# Convert word → RGB using hash → match to token
def word_to_color_token(word, token_map):
    # Generate RGB from hash
    h = hashlib.sha256(word.encode()).digest()
    r, g, b = h[0], h[1], h[2]

    # Nearest match from token_map (or exact if exists)
    closest_rgb = min(token_map.keys(), key=lambda k: (k[0]-r)**2 + (k[1]-g)**2 + (k[2]-b)**2)
    return token_map[closest_rgb]
