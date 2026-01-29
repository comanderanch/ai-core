"""
Load semantic pairs from expanded_semantic_pairs.txt
"""
import numpy as np
from pathlib import Path
from typing import Tuple, List, Dict
import json

class ExpandedPairLoader:
    """Load 1.9M semantic pairs from file."""
    
    def __init__(
        self, 
        vectors_498d: np.ndarray,
        word_to_token: Dict[str, int],
        pairs_file: str = "expanded_semantic_pairs.txt",
        max_pairs: int = 100000
    ):
        """
        Initialize pair loader.
        
        Args:
            vectors_498d: All 498D token vectors (2304, 498)
            word_to_token: Word to token ID mapping
            pairs_file: Path to semantic pairs file
            max_pairs: Maximum pairs to load (for training efficiency)
        """
        self.vectors = vectors_498d
        self.word_to_token = word_to_token
        self.pairs_file = Path(pairs_file)
        self.max_pairs = max_pairs
        
        self.pairs = self._load_pairs()
        
        print(f"[✓] ExpandedPairLoader initialized")
        print(f"    Loaded pairs: {len(self.pairs):,}")
        print(f"    From file: {self.pairs_file}")
    
    def _load_pairs(self) -> List[Tuple[int, int]]:
        """Load word pairs and convert to token IDs."""
        pairs = []
        skipped = 0
        
        with open(self.pairs_file, 'r') as f:
            for line in f:
                if len(pairs) >= self.max_pairs:
                    break
                
                parts = line.strip().split('\t')
                if len(parts) != 2:
                    continue
                
                pair_str, count = parts
                word1, word2 = pair_str.split(':')
                
                # Convert words to token IDs
                token1 = self.word_to_token.get(word1)
                token2 = self.word_to_token.get(word2)
                
                if token1 is not None and token2 is not None:
                    pairs.append((token1, token2))
                else:
                    skipped += 1
        
        if skipped > 0:
            print(f"    Skipped {skipped:,} pairs (words not in vocabulary)")
        
        return pairs
    
    def generate_training_data(
        self, 
        num_samples: int = 100000
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate training data from loaded pairs.
        
        Args:
            num_samples: Number of training samples to generate
        
        Returns:
            (inputs, targets): Arrays of shape (num_samples, 498)
        """
        print(f"[*] Generating {num_samples:,} training samples...")
        
        inputs = []
        targets = []
        
        # Sample from loaded pairs
        for _ in range(num_samples):
            # Random pair
            token1, token2 = self.pairs[np.random.randint(len(self.pairs))]
            
            # Input = token1 vector, Target = token2 vector
            inputs.append(self.vectors[token1])
            targets.append(self.vectors[token2])
        
        inputs = np.array(inputs, dtype=np.float32)
        targets = np.array(targets, dtype=np.float32)
        
        print(f"[✓] Generated {len(inputs):,} training pairs")
        
        return inputs, targets

def load_word_to_token_map(tokenizer_dir: str = "../tokenizer") -> Dict[str, int]:
    """Load word-to-token mapping from tokenizer."""
    map_file = Path(tokenizer_dir) / "word_token_map.json"
    
    if not map_file.exists():
        print(f"[!] Warning: {map_file} not found")
        return {}
    
    with open(map_file, 'r') as f:
        data = json.load(f)
    
    # Extract word_to_tokens and flatten
    word_to_tokens = data.get("word_to_tokens", {})
    
    word_to_token = {}
    for word, token_list in word_to_tokens.items():
        if token_list and len(token_list) > 0:
            word_to_token[word] = token_list[0]  # Use first token
    
    print(f"[✓] Loaded word-to-token map: {len(word_to_token):,} words")
    
    return word_to_token

if __name__ == "__main__":
    # Test loading
    print("Testing expanded pair loader...")
    print()
    
    # Load vectors
    vectors = np.load("../tokenizer/token_vectors_498d.npy")
    print(f"[✓] Loaded {len(vectors)} token vectors")
    
    # Load word map
    word_to_token = load_word_to_token_map()
    
    # Load pairs
    loader = ExpandedPairLoader(
        vectors_498d=vectors,
        word_to_token=word_to_token,
        max_pairs=100000
    )
    
    # Generate sample
    print()
    inputs, targets = loader.generate_training_data(num_samples=1000)
    print(f"[✓] Sample input shape: {inputs.shape}")
    print(f"[✓] Sample target shape: {targets.shape}")
    print()
    print("✅ Loader working correctly!")
