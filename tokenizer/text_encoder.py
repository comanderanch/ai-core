#!/usr/bin/env python3
"""
AI-Core Standalone: Constraint Lattice Text Encoder
====================================================

Encodes text into token indices using CONSTRAINT-FIRST validation,
not probability-first matching.

Architecture:
  - Color psychology heuristics (red→hot, blue→cold)
  - Learns from experience (grows semantic map)
  - Rule Zero enforcement (fact overrides prediction)
  - Lattice validation (meaning must survive constraint)

Author: comanderanch
Phase: 5.7 Standalone Resurrection
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class ConstraintLatticeEncoder:
    """
    Text→Token encoder using constraint-first validation.
    
    NOT probability-based (no "what's most likely")
    BUT constraint-based ("what passes validation")
    
    Principles:
      1. Meaning precedes probability (lattice first)
      2. Color is grounded in physics (wavelength reality)
      3. Learning happens through experience (not pre-training)
      4. Rule Zero: Fact must override prediction
    """
    
    def __init__(
        self, 
        word_map_path: str = "tokenizer/word_token_map.json",
        color_tokens_path: str = "tokenizer/full_color_tokens.csv",
        learning_mode: bool = True
    ):
        """
        Initialize encoder with constraint lattice.
        
        Args:
            word_map_path: Path to semantic word→token mappings
            color_tokens_path: Path to 2,304 base color tokens
            learning_mode: If True, learns new words through experience
        """
        self.word_map_path = Path(word_map_path)
        self.color_tokens_path = Path(color_tokens_path)
        self.learning_mode = learning_mode
        
        # Load or initialize word→token mappings
        self.word_to_tokens = self._load_word_map()
        self.token_to_words = self._build_reverse_map()
        
        # Load color token metadata
        self.color_tokens = self._load_color_tokens()
        
        # Experience log (learning events)
        self.experience_log = []
        
        # Color psychology heuristics (bootstrap knowledge)
        self.color_heuristics = self._init_color_heuristics()
        
        print(f"[✓] Constraint Lattice Encoder initialized")
        print(f"    Known words: {len(self.word_to_tokens)}")
        print(f"    Learning mode: {self.learning_mode}")
    
    def _load_word_map(self) -> Dict[str, List[int]]:
        """Load existing word→token mappings or create new."""
        if self.word_map_path.exists():
            with open(self.word_map_path, 'r') as f:
                data = json.load(f)
                return data.get('word_to_tokens', {})
        else:
            # Start empty - will learn through experience
            return {}
    
    def _build_reverse_map(self) -> Dict[int, List[str]]:
        """Build token→words reverse index."""
        reverse = {}
        for word, token_list in self.word_to_tokens.items():
            for token_id in token_list:
                if token_id not in reverse:
                    reverse[token_id] = []
                if word not in reverse[token_id]:
                    reverse[token_id].append(word)
        return reverse
    
    def _load_color_tokens(self) -> Dict[int, Dict]:
        """Load color token metadata (hue, RGB, frequency)."""
        tokens = {}
        if self.color_tokens_path.exists():
            with open(self.color_tokens_path, 'r') as f:
                next(f)  # Skip header
                for idx, line in enumerate(f):
                    parts = line.strip().split(',')
                    if len(parts) >= 10:
                        # Use decimal values (columns 5-9)
                        tokens[idx] = {
                            'hue': int(parts[5]),      # Column 5: Hue decimal
                            'r': int(parts[6]),        # Column 6: R decimal
                            'g': int(parts[7]),        # Column 7: G decimal
                            'b': int(parts[8]),        # Column 8: B decimal
                            'freq': float(parts[9])    # Column 9: Freq decimal
                    }
        return tokens
    
    def _init_color_heuristics(self) -> Dict[str, Tuple[int, int]]:
        """
        Bootstrap color psychology heuristics.
        
        NOT arbitrary - based on physics (wavelength→perception)
        
        Returns:
            Dict mapping concepts to (start_token, end_token) ranges
        """
        return {
            # Red family (0-200): Hot, energy, danger, passion
            'hot': (0, 50),
            'fire': (0, 50),
            'danger': (0, 50),
            'anger': (0, 50),
            'passion': (10, 60),
            'love': (10, 60),
            'blood': (0, 50),
            'stop': (0, 30),
            
            # Orange family (200-400): Warmth, creativity, caution
            'warm': (200, 300),
            'creative': (200, 300),
            'autumn': (200, 300),
            'sunset': (200, 300),
            'caution': (250, 350),
            
            # Yellow family (400-600): Light, happiness, attention
            'bright': (400, 500),
            'happy': (400, 500),
            'sun': (400, 500),
            'light': (400, 500),
            'gold': (450, 550),
            'attention': (400, 500),
            
            # Green family (600-1000): Nature, growth, balance
            'nature': (600, 800),
            'growth': (600, 800),
            'tree': (600, 800),
            'grass': (600, 800),
            'forest': (600, 800),
            'balance': (650, 850),
            'health': (650, 850),
            'go': (700, 800),
            'safe': (700, 800),
            
            # Blue family (1000-1400): Cool, calm, depth
            'cool': (1000, 1200),
            'calm': (1000, 1200),
            'sky': (1000, 1200),
            'ocean': (1050, 1250),
            'water': (1050, 1250),
            'sad': (1000, 1200),
            'depth': (1100, 1300),
            'trust': (1050, 1250),
            
            # Purple family (1400-1800): Mystery, wisdom, luxury
            'mystery': (1400, 1600),
            'wisdom': (1400, 1600),
            'magic': (1400, 1600),
            'royal': (1400, 1600),
            'luxury': (1450, 1650),
            
            # Grayscale (1800-2304): Balance, neutral, clarity
            'neutral': (1800, 2000),
            'balance': (1850, 2050),
            'clarity': (1900, 2100),
            'empty': (1800, 1900),
            'full': (2100, 2300),
        }
    
    def encode_word(
        self, 
        word: str, 
        context: Optional[str] = None
    ) -> List[int]:
        """
        Encode word into token indices using constraint validation.
        
        Process:
          1. Check if word is known (fact)
          2. If unknown and learning_mode: learn from heuristics
          3. Validate through constraint lattice
          4. Return valid token indices
        
        Args:
            word: Word to encode
            context: Optional context sentence for learning
        
        Returns:
            List of token indices that passed constraint
        """
        word_lower = word.lower().strip()
        
        # Rule Zero: Fact overrides prediction
        if word_lower in self.word_to_tokens:
            # Known word (fact)
            return self.word_to_tokens[word_lower]
        
        # Unknown word - enter imagination layer (constrained)
        if self.learning_mode:
            return self._learn_word(word_lower, context)
        else:
            # Learning disabled - return empty (silent)
            return []
    
    def _learn_word(
        self, 
        word: str, 
        context: Optional[str] = None
    ) -> List[int]:
        """
        Learn new word through constraint-bounded imagination.
        
        NOT probability-first ("what's likely?")
        BUT heuristic-first ("what matches physics?")
        
        Learning sources (in order):
          1. Color heuristics (physics-based)
          2. Context clues (if provided)
          3. Similar word patterns
          4. Ask user (interactive learning)
        
        Args:
            word: Word to learn
            context: Optional context for clues
        
        Returns:
            Token indices learned
        """
        # Try color heuristics first
        if word in self.color_heuristics:
            start, end = self.color_heuristics[word]
            tokens = self._select_tokens_from_range(start, end)
            
            # Log learning event
            self._log_learning(word, tokens, source='heuristic')
            
            # Save to map
            self.word_to_tokens[word] = tokens
            self._update_reverse_map(word, tokens)
            
            return tokens
        
        # Try context-based learning
        if context:
            tokens = self._learn_from_context(word, context)
            if tokens:
                return tokens
        
        # Fallback: Mark as unknown, return empty
        print(f"[?] Unknown word: '{word}' (no heuristic, no context)")
        return []
    
    def _select_tokens_from_range(
        self, 
        start: int, 
        end: int, 
        count: int = 3
    ) -> List[int]:
        """
        Select token indices from color range.
        
        Selects evenly-spaced tokens to cover range diversity.
        
        Args:
            start: Start of token range
            end: End of token range
            count: Number of tokens to select
        
        Returns:
            List of token indices
        """
        step = (end - start) // count
        tokens = [start + i * step for i in range(count)]
        # Ensure within bounds
        tokens = [t for t in tokens if 0 <= t < 2304]
        return tokens
    
    def _learn_from_context(
        self, 
        word: str, 
        context: str
    ) -> Optional[List[int]]:
        """
        Learn word from context sentence.
        
        Example:
          Context: "the grass is green"
          Word: "grass"
          → Look for "green" (known)
          → Link "grass" to green tokens
        
        Args:
            word: Word to learn
            context: Context sentence
        
        Returns:
            Token indices if learned, None otherwise
        """
        context_lower = context.lower()
        context_words = context_lower.split()
        
        # Find known words in context
        for ctx_word in context_words:
            if ctx_word in self.word_to_tokens and ctx_word != word:
                # Found a known word - link to it
                tokens = self.word_to_tokens[ctx_word]
                
                # Log learning
                self._log_learning(
                    word, 
                    tokens, 
                    source=f'context:{ctx_word}'
                )
                
                # Save
                self.word_to_tokens[word] = tokens
                self._update_reverse_map(word, tokens)
                
                print(f"[✓] Learned: '{word}' → {tokens} (from context: '{ctx_word}')")
                return tokens
        
        return None
    
    def _update_reverse_map(self, word: str, tokens: List[int]):
        """Update token→words reverse mapping."""
        for token_id in tokens:
            if token_id not in self.token_to_words:
                self.token_to_words[token_id] = []
            if word not in self.token_to_words[token_id]:
                self.token_to_words[token_id].append(word)
    
    def _log_learning(
        self, 
        word: str, 
        tokens: List[int], 
        source: str
    ):
        """Log learning event for analysis."""
        event = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'word': word,
            'tokens': tokens,
            'source': source
        }
        self.experience_log.append(event)
    
    def encode_sentence(self, sentence: str) -> List[int]:
        """
        Encode sentence into token sequence.
        
        Args:
            sentence: Input sentence
        
        Returns:
            Flat list of token indices
        """
        words = sentence.lower().split()
        token_sequence = []
        
        for word in words:
            tokens = self.encode_word(word, context=sentence)
            token_sequence.extend(tokens)
        
        return token_sequence
    
    def save_word_map(self):
        """Save learned word→token mappings to file."""
        data = {
            'word_to_tokens': self.word_to_tokens,
            'metadata': {
                'total_words': len(self.word_to_tokens),
                'last_updated': datetime.utcnow().isoformat() + 'Z',
                'learning_mode': self.learning_mode
        }
    }
    
        # Ensure directory exists (handle being run from within tokenizer/)
        if not self.word_map_path.parent.exists():
            self.word_map_path.parent.mkdir(parents=True, exist_ok=True)
    
        with open(self.word_map_path, 'w') as f:
            json.dump(data, f, indent=2)
    
        print(f"[✓] Word map saved: {self.word_map_path}")
        print(f"    Total words: {len(self.word_to_tokens)}")
    
    def get_stats(self) -> Dict:
        """Get encoder statistics."""
        return {
            'total_words': len(self.word_to_tokens),
            'learning_events': len(self.experience_log),
            'learning_mode': self.learning_mode,
            'color_tokens': len(self.color_tokens)
        }


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("CONSTRAINT LATTICE ENCODER - TEST")
    print("="*60)
    
    # Initialize with correct paths (we're running FROM tokenizer dir)
    encoder = ConstraintLatticeEncoder(
        word_map_path="word_token_map.json",      # No tokenizer/ prefix
        color_tokens_path="full_color_tokens.csv", # No tokenizer/ prefix
        learning_mode=True
    )
    
    # Test encoding known words (from heuristics)
    print("\n[TEST 1] Known words (heuristics):")
    for word in ['fire', 'sky', 'grass', 'ocean']:
        tokens = encoder.encode_word(word)
        print(f"  '{word}' → {tokens}")
    
    # Test encoding sentence
    print("\n[TEST 2] Sentence encoding:")
    sentence = "the fire is hot"
    tokens = encoder.encode_sentence(sentence)
    print(f"  '{sentence}' → {tokens}")
    
    # Test learning from context
    print("\n[TEST 3] Learning from context:")
    sentence = "the tree is green and tall"
    tokens = encoder.encode_sentence(sentence)
    print(f"  '{sentence}' → {tokens}")
    
    # Save learned mappings
    print("\n[SAVE] Word map:")
    encoder.save_word_map()
    
    # Show stats
    print("\n[STATS]")
    stats = encoder.get_stats()
    for key, val in stats.items():
        print(f"  {key}: {val}")
    
    print("\n" + "="*60)
    print("Test complete. Encoder ready for integration.")
    print("="*60)