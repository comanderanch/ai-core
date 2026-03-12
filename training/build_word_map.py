#!/usr/bin/env python3
"""
AI-Core Standalone: Build Complete Word→Token Map
==================================================

Rebuilds word_token_map.json from the semantic training pairs
so the decoder can translate ALL tokens the model predicts.

Author: comanderanch
Phase: 5.7 Standalone Resurrection
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


def build_word_map_from_pairs(
    pairs_file: str = "training/massive_semantic_pairs.txt",
    output_file: str = "tokenizer/word_token_map.json"
):
    """
    Build complete word→token mapping from training pairs.
    
    Args:
        pairs_file: Semantic pairs file
        output_file: Output word map JSON
    """
    print("="*60)
    print("BUILDING COMPLETE WORD→TOKEN MAP")
    print("="*60)
    
    word_to_tokens = {}
    token_to_words = defaultdict(list)
    
    print(f"\n[*] Reading pairs from: {pairs_file}")
    
    pairs_count = 0
    with open(pairs_file, 'r') as f:
        for line in f:
            # Skip comments
            if line.startswith('#'):
                continue
            
            parts = line.strip().split()
            if len(parts) != 4:
                continue
            
            word1, word2, tokens1_str, tokens2_str = parts
            
            # Parse tokens
            tokens1 = [int(t) for t in tokens1_str.split(',')]
            tokens2 = [int(t) for t in tokens2_str.split(',')]
            
            # Add to mappings
            word_to_tokens[word1] = tokens1
            word_to_tokens[word2] = tokens2
            
            # Build reverse map
            for token in tokens1:
                if word1 not in token_to_words[token]:
                    token_to_words[token].append(word1)
            
            for token in tokens2:
                if word2 not in token_to_words[token]:
                    token_to_words[token].append(word2)
            
            pairs_count += 1
    
    print(f"[✓] Processed {pairs_count} pairs")
    print(f"[✓] Extracted {len(word_to_tokens)} unique words")
    print(f"[✓] Mapped {len(token_to_words)} unique tokens")
    
    # Save word→token map
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        'word_to_tokens': word_to_tokens,
        'metadata': {
            'total_words': len(word_to_tokens),
            'total_tokens_mapped': len(token_to_words),
            'source': 'massive_semantic_pairs.txt',
            'generated': datetime.utcnow().isoformat() + 'Z'
        }
    }
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n[✓] Word map saved: {output_path}")
    print(f"    Total words: {len(word_to_tokens)}")
    
    # Show sample of token 1250 mappings
    if 1250 in token_to_words:
        print(f"\n[*] Token 1250 maps to: {token_to_words[1250][:10]}")
    
    # Show coverage stats
    print(f"\n[*] Coverage statistics:")
    tokens_per_word = [len(tokens) for tokens in word_to_tokens.values()]
    avg_tokens = sum(tokens_per_word) / len(tokens_per_word)
    print(f"    Average tokens per word: {avg_tokens:.1f}")
    
    words_per_token = [len(words) for words in token_to_words.values()]
    avg_words = sum(words_per_token) / len(words_per_token)
    print(f"    Average words per token: {avg_words:.1f}")
    
    print("\n" + "="*60)
    print("WORD MAP COMPLETE")
    print("="*60)


if __name__ == "__main__":
    build_word_map_from_pairs()