#!/usr/bin/env python3
"""
Add psychology terms to AI-Core vocabulary.
"""

import json
import numpy as np
from pathlib import Path

def load_existing_vocabulary():
    """Load current word-token map."""
    with open('tokenizer/word_token_map.json', 'r') as f:
        data = json.load(f)
    
    word_to_tokens = data.get('word_to_tokens', {})
    print(f"Current vocabulary: {len(word_to_tokens)} words")
    
    return word_to_tokens, data

def extract_psychology_words():
    """Extract all unique words from psychology pairs."""
    words = set()
    
    files = [
        'training_data/psychology_pairs_cognitive.txt',
        'training_data/psychology_pairs_book.txt'
    ]
    
    for file in files:
        if Path(file).exists():
            with open(file, 'r') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        words.add(parts[0].lower())
                        words.add(parts[1].lower())
    
    print(f"Psychology terms found: {len(words)}")
    return words

def generate_498d_vector_for_word(word):
    """
    Generate a 498D vector for a word.
    
    CORRECT dimensions:
    41 (base) + 41 (influence) + 166 (quantum) + 250 (grid) = 498D
    """
    # Create deterministic hash from word
    hash_val = hash(word) % (2**31)
    
    # Use hash as seed for reproducible random vector
    np.random.seed(hash_val)
    
    # Generate 498D vector with CORRECT dimensions
    base = np.random.randn(41)
    influence = np.random.randn(41)
    quantum = np.random.randn(166)  # Was 164, should be 166!
    grid = np.random.randn(250)
    
    vector = np.concatenate([base, influence, quantum, grid])
    
    # Verify dimension
    assert vector.shape[0] == 498, f"Wrong dimension: {vector.shape[0]}"
    
    # Normalize
    vector = vector / (np.linalg.norm(vector) + 1e-8)
    
    return vector.astype(np.float32)

def add_psychology_terms():
    """Add psychology terms to vocabulary and generate vectors."""
    
    print("="*70)
    print("ADDING PSYCHOLOGY TERMS TO VOCABULARY")
    print("="*70)
    print()
    
    # Load existing
    word_to_tokens, data = load_existing_vocabulary()
    
    # Load existing vectors
    existing_vectors = np.load('tokenizer/token_vectors_498d.npy')
    print(f"Existing vectors shape: {existing_vectors.shape}")
    
    # Extract psychology words
    psych_words = extract_psychology_words()
    
    # Find which are missing
    missing_words = [w for w in psych_words if w not in word_to_tokens]
    print(f"Missing from vocabulary: {len(missing_words)}")
    print()
    
    if not missing_words:
        print("✅ All psychology words already in vocabulary!")
        return
    
    # Show sample
    print("Sample words being added:")
    for word in sorted(missing_words)[:20]:
        print(f"  - {word}")
    if len(missing_words) > 20:
        print(f"  ... and {len(missing_words)-20} more")
    print()
    
    # Get next available token ID
    max_token = max([t for tokens in word_to_tokens.values() for t in tokens])
    next_token = max_token + 1
    
    print(f"Starting token ID: {next_token}")
    print("Generating 498D vectors...")
    print()
    
    # Generate vectors for new words
    new_vectors = []
    added_count = 0
    
    for word in sorted(missing_words):
        # Generate 498D vector
        vector = generate_498d_vector_for_word(word)
        new_vectors.append(vector)
        
        # Add to vocabulary
        word_to_tokens[word] = [next_token]
        next_token += 1
        added_count += 1
        
        if added_count % 10 == 0:
            print(f"  Added {added_count}/{len(missing_words)} words...")
    
    print(f"✅ Added {added_count} words")
    print()
    
    # Combine vectors
    new_vectors = np.array(new_vectors)
    print(f"New vectors shape: {new_vectors.shape}")
    
    combined_vectors = np.vstack([existing_vectors, new_vectors])
    
    print(f"Combined vectors shape: {combined_vectors.shape}")
    print(f"New vocabulary size: {len(word_to_tokens)}")
    print()
    
    # Save updated vocabulary
    data['word_to_tokens'] = word_to_tokens
    
    with open('tokenizer/word_token_map.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✅ Saved: tokenizer/word_token_map.json")
    
    # Save updated vectors
    np.save('tokenizer/token_vectors_498d.npy', combined_vectors)
    
    print("✅ Saved: tokenizer/token_vectors_498d.npy")
    print()
    
    # Verify
    print("Verification:")
    test_words = ['disorder', 'anxiety', 'therapy', 'personality', 'stress']
    for word in test_words:
        if word in word_to_tokens:
            token = word_to_tokens[word][0]
            print(f"  ✅ '{word}' → token {token}")
        else:
            print(f"  ❌ '{word}' not found")
    
    print()
    print("="*70)
    print("✅ VOCABULARY EXPANSION COMPLETE!")
    print("="*70)

if __name__ == "__main__":
    add_psychology_terms()
