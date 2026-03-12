#!/usr/bin/env python3
"""
AI-Core Standalone: Text Decoder
=================================

Decodes token indices back into human-readable text.

Architecture:
  - Reverse lookup from word_token_map.json
  - Handles multiple words per token (ambiguity resolution)
  - Context-aware word selection
  - Fallback to token IDs for unknown tokens

Author: comanderanch
Phase: 5.7 Standalone Resurrection
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class TextDecoder:
    """
    Token indices → Text decoder using reverse word map.
    
    Decodes MinimalLLM output back into human language.
    
    Principles:
      1. Use learned word associations (from encoder)
      2. Handle ambiguity (one token → multiple words)
      3. Context-aware selection (best word for sequence)
      4. Graceful fallback (unknown tokens → IDs)
    """
    
    def __init__(
        self, 
        word_map_path: str = "tokenizer/word_token_map.json"
    ):
        """
        Initialize decoder with word→token mappings.
        
        Args:
            word_map_path: Path to word_token_map.json from encoder
        """
        self.word_map_path = Path(word_map_path)
        
        # Load word→token map from encoder
        self.word_to_tokens = self._load_word_map()
        
        # Build reverse map: token→words
        self.token_to_words = self._build_reverse_map()
        
        print(f"[✓] Text Decoder initialized")
        print(f"    Known words: {len(self.word_to_tokens)}")
        print(f"    Token mappings: {len(self.token_to_words)}")
    
    def _load_word_map(self) -> Dict[str, List[int]]:
        """Load word→token mappings from encoder."""
        if self.word_map_path.exists():
            with open(self.word_map_path, 'r') as f:
                data = json.load(f)
                return data.get('word_to_tokens', {})
        else:
            print(f"[!] Warning: No word map found at {self.word_map_path}")
            return {}
    
    def _build_reverse_map(self) -> Dict[int, List[str]]:
        """
        Build token→words reverse index.
        
        One token can map to multiple words:
          Token 0 might be: ['fire', 'hot', 'danger']
        
        Returns:
            Dict mapping token_id → list of possible words
        """
        reverse = {}
        for word, token_list in self.word_to_tokens.items():
            for token_id in token_list:
                if token_id not in reverse:
                    reverse[token_id] = []
                if word not in reverse[token_id]:
                    reverse[token_id].append(word)
        return reverse
    
    def decode_token(
        self, 
        token_id: int, 
        context: Optional[List[str]] = None
    ) -> str:
        """
        Decode single token to word.
        
        Args:
            token_id: Token index to decode
            context: Previous words in sequence (for disambiguation)
        
        Returns:
            Best matching word or fallback to token ID
        """
        if token_id not in self.token_to_words:
            # Unknown token - return as ID
            return f"<token_{token_id}>"
        
        possible_words = self.token_to_words[token_id]
        
        if len(possible_words) == 1:
            # Only one option - use it
            return possible_words[0]
        
        # Multiple options - use context to pick best
        if context:
            return self._select_by_context(possible_words, context)
        else:
            # No context - return first option
            return possible_words[0]
    
    def _select_by_context(
        self, 
        possible_words: List[str], 
        context: List[str]
    ) -> str:
        """
        Select best word from options using context.
        
        Simple heuristic:
          - Avoid repeating the last word
          - Prefer words not in recent context
        
        Args:
            possible_words: List of candidate words
            context: Recent words in sequence
        
        Returns:
            Best word choice
        """
        # Avoid immediate repetition
        if context:
            last_word = context[-1]
            others = [w for w in possible_words if w != last_word]
            if others:
                return others[0]
        
        # Default to first option
        return possible_words[0]
    
    def decode_tokens(
        self, 
        token_ids: List[int]
    ) -> str:
        """
        Decode sequence of tokens into sentence.
        
        Args:
            token_ids: List of token indices
        
        Returns:
            Decoded sentence
        """
        if not token_ids:
            return ""
        
        words = []
        for token_id in token_ids:
            word = self.decode_token(token_id, context=words)
            words.append(word)
        
        # Join into sentence
        sentence = ' '.join(words)
        return sentence
    
    def decode_with_confidence(
        self, 
        token_ids: List[int]
    ) -> List[Tuple[str, float]]:
        """
        Decode tokens with confidence scores.
        
        Confidence = 1.0 if token maps to single word
        Confidence = 1.0/n if token maps to n words (ambiguity)
        
        Args:
            token_ids: List of token indices
        
        Returns:
            List of (word, confidence) tuples
        """
        results = []
        
        for token_id in token_ids:
            if token_id not in self.token_to_words:
                # Unknown token
                results.append((f"<token_{token_id}>", 0.0))
            else:
                possible = self.token_to_words[token_id]
                confidence = 1.0 / len(possible)
                word = possible[0]  # Take first option
                results.append((word, confidence))
        
        return results
    
    def get_all_options(self, token_id: int) -> List[str]:
        """
        Get all possible words for a token.
        
        Useful for debugging or interactive disambiguation.
        
        Args:
            token_id: Token index
        
        Returns:
            List of all possible words
        """
        return self.token_to_words.get(token_id, [])
    
    def get_stats(self) -> Dict:
        """Get decoder statistics."""
        ambiguous_tokens = sum(
            1 for words in self.token_to_words.values() 
            if len(words) > 1
        )
        
        return {
            'total_words': len(self.word_to_tokens),
            'mapped_tokens': len(self.token_to_words),
            'ambiguous_tokens': ambiguous_tokens,
            'avg_words_per_token': (
                sum(len(w) for w in self.token_to_words.values()) / 
                max(len(self.token_to_words), 1)
            )
        }


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("TEXT DECODER - TEST")
    print("="*60)
    
    # Initialize decoder
    decoder = TextDecoder()
    
    # Test decoding individual tokens
    print("\n[TEST 1] Decode individual tokens:")
    test_tokens = [0, 16, 32, 600, 666, 732, 1000, 1066, 1132]
    for token_id in test_tokens:
        word = decoder.decode_token(token_id)
        options = decoder.get_all_options(token_id)
        print(f"  Token {token_id:4d} → '{word}' (options: {options})")
    
    # Test decoding sequence (from encoder test)
    print("\n[TEST 2] Decode token sequence:")
    # From encoder: "the fire is hot" → [0, 16, 32, 0, 16, 32, 0, 16, 32, 0, 16, 32]
    sequence = [0, 16, 32, 0, 16, 32, 0, 16, 32, 0, 16, 32]
    decoded = decoder.decode_tokens(sequence)
    print(f"  Tokens: {sequence}")
    print(f"  Decoded: '{decoded}'")
    
    # Test with confidence scores
    print("\n[TEST 3] Decode with confidence:")
    results = decoder.decode_with_confidence([0, 600, 1000])
    for word, confidence in results:
        print(f"  '{word}' (confidence: {confidence:.2f})")
    
    # Show statistics
    print("\n[STATS]")
    stats = decoder.get_stats()
    for key, val in stats.items():
        if isinstance(val, float):
            print(f"  {key}: {val:.2f}")
        else:
            print(f"  {key}: {val}")
    
    print("\n" + "="*60)
    print("Test complete. Decoder ready for integration.")
    print("="*60)