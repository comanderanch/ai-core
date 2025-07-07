import os

# Define the list of token indices you want to log
token_indices = [10, 15, 20, 25, 30]

for index in token_indices:
    print(f"\n▶ Logging token {index}...")
    os.system(f"python3 inference.py {index}")
