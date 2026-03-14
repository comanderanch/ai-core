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

            # Green plane — ethical care vocabulary (650-850): ethics_001 domain
            'care': (650, 800),
            'heal': (650, 800),
            'help': (650, 800),
            'ethical': (650, 850),
            'right': (700, 800),

            # Red plane — harm/danger signals (0-100): harm maps to red, not green
            'harm': (0, 100),
            'wrong': (0, 100),

            # Violet plane — wisdom ethics (1400-1600)
            'moral': (1400, 1600),
            'justice': (1400, 1600),

            # Blue plane — logical obligation (1050-1250)
            'duty': (1050, 1250),

            # Gray plane — balance/fairness (1850-2050)
            'fair': (1850, 2050),
            
            # Blue family (1000-1400): Cool, calm, depth
            'cool': (1000, 1200),
            'calm': (1000, 1200),
            'sky': (1000, 1200),
            'ocean': (1050, 1250),
            'water': (1050, 1250),
            'sad': (1000, 1200),
            'depth': (1100, 1300),
            'trust': (1050, 1250),

            # Blue plane — logical connectives (1000-1300): logic_001 / language_001 domain
            'if': (1000, 1200),
            'then': (1000, 1200),
            'implies': (1050, 1250),
            'and': (1000, 1200),
            'or': (1000, 1200),
            'not': (1000, 1100),
            'all': (1100, 1300),
            'every': (1100, 1300),
            'some': (1050, 1250),
            'none': (1000, 1100),
            'therefore': (1100, 1300),
            'because': (1050, 1250),
            'when': (1000, 1200),
            'unless': (1050, 1250),
            'until': (1050, 1250),
            'while': (1000, 1200),
            'since': (1050, 1250),

            # Blue plane — mathematical operators (1050-1250): logic_001 domain
            'equals': (1050, 1250),
            'plus': (1050, 1250),
            'minus': (1050, 1250),
            'times': (1050, 1250),
            'divided': (1050, 1250),
            'greater': (1100, 1300),
            'less': (1000, 1100),
            'zero': (1050, 1250),
            'one': (1050, 1250),
            'true': (1100, 1300),
            'false': (1000, 1100),

            # Purple family (1400-1800): Mystery, wisdom, luxury
            'mystery': (1400, 1600),
            'wisdom': (1400, 1600),
            'magic': (1400, 1600),
            'royal': (1400, 1600),
            'luxury': (1450, 1650),
            
            # Grayscale (1800-2304): Balance, neutral, clarity
            'neutral': (1800, 2000),
            'clarity': (1900, 2100),
            'empty': (1800, 1900),
            'full': (2100, 2300),

            # Neutral gray — identity/structure words (1800-2100): copulas, determiners
            'is': (1900, 2100),
            'are': (1900, 2100),
            'was': (1850, 2050),
            'were': (1850, 2050),
            'be': (1900, 2100),
            'been': (1900, 2100),
            'being': (1850, 2050),
            'the': (1800, 2000),
            'a': (1800, 2000),
            'an': (1800, 2000),
            'this': (1850, 2050),
            'that': (1850, 2050),
            'these': (1850, 2050),
            'those': (1850, 2050),

            # Interrogative pronouns — gray plane (1800-2100)
            'what':  (1800, 2100),
            'where': (1800, 2100),
            'when':  (1800, 2100),
            'how':   (1800, 2100),
            'why':   (1800, 2100),
            'which': (1800, 2100),
            'who':   (1800, 2100),
            'whom':  (1800, 2100),
            'whose': (1800, 2100),
            'way':   (1800, 2100),

            # Personal pronouns — gray plane (1800-2100)
            'i':     (1800, 2100),
            'you':   (1800, 2100),
            'me':    (1800, 2100),
            'my':    (1800, 2100),
            'mine':  (1800, 2100),
            'we':    (1800, 2100),
            'us':    (1800, 2100),
            'our':   (1800, 2100),
            'ours':  (1800, 2100),
            'they':  (1800, 2100),
            'them':  (1800, 2100),
            'their': (1800, 2100),
            'theirs':(1800, 2100),
            'he':    (1800, 2100),
            'him':   (1800, 2100),
            'his':   (1800, 2100),
            'she':   (1800, 2100),
            'her':   (1800, 2100),
            'hers':  (1800, 2100),
            'it':    (1800, 2100),
            'its':   (1800, 2100),
            'itself':(1800, 2100),
            'myself':(1800, 2100),
            'yourself': (1800, 2100),

            # Auxiliary verbs — gray plane (1800-2100)
            'do':     (1800, 2100),
            'does':   (1800, 2100),
            'did':    (1800, 2100),
            'am':     (1800, 2100),
            'have':   (1800, 2100),
            'has':    (1800, 2100),
            'had':    (1800, 2100),
            'will':   (1800, 2100),
            'would':  (1800, 2100),
            'could':  (1800, 2100),
            'should':  (1800, 2100),
            'can':    (1800, 2100),
            'may':    (1800, 2100),
            'might':  (1800, 2100),
            'shall':  (1800, 2100),
            'must':   (1800, 2100),
            'not':    (1800, 2100),
            'no':     (1800, 2100),
            'yes':    (1800, 2100),
            'get':    (1800, 2100),
            'got':    (1800, 2100),

            # Common structural words — gray plane (1800-2100)
            'all':    (1800, 2100),
            'more':   (1800, 2100),
            'just':   (1800, 2100),
            'also':   (1800, 2100),
            'only':   (1800, 2100),
            'than':   (1800, 2100),
            'then':   (1800, 2100),
            'now':    (1800, 2100),
            'here':   (1800, 2100),
            'there':  (1800, 2100),
            'about':  (1800, 2100),
            'up':     (1800, 2100),
            'out':    (1800, 2100),
            'over':   (1800, 2100),
            'after':  (1800, 2100),
            'before': (1800, 2100),
            'between':(1800, 2100),
            'through':(1800, 2100),
            'during': (1800, 2100),
            'like':   (1800, 2100),
            'very':   (1800, 2100),
            'much':   (1800, 2100),
            'many':   (1800, 2100),
            'any':    (1800, 2100),
            'each':   (1800, 2100),
            'both':   (1800, 2100),
            'same':   (1800, 2100),
            'such':   (1800, 2100),
            'own':    (1800, 2100),
            'other':  (1800, 2100),
            'another':(1800, 2100),
            'hello':  (1800, 2100),
            'hi':     (1800, 2100),
            'ok':     (1800, 2100),
            'okay':   (1800, 2100),

            # Structural prepositions — gray plane (1800-2100)
            'of':   (1800, 2100),
            'in':   (1800, 2100),
            'at':   (1800, 2100),
            'to':   (1800, 2100),
            'for':  (1800, 2100),
            'with': (1800, 2100),
            'by':   (1800, 2100),
            'from': (1800, 2100),
            'on':   (1800, 2100),
            'as':   (1800, 2100),
            'into': (1800, 2100),
            'onto': (1800, 2100),
            'upon': (1800, 2100),
            'but':  (1800, 2100),
            'yet':  (1800, 2100),
            'so':   (1800, 2100),
            'nor':  (1800, 2100),

            # AIA technical vocabulary — mapped to their planes
            'resonance':   (1400, 1600),  # violet — memory/frequency concept
            'frequency':   (1400, 1600),
            'frequencies': (1400, 1600),
            'memory':      (1400, 1600),
            'memories':    (1400, 1600),
            'emotion':     (0,    200),   # red — emotion plane
            'emotional':   (0,    200),
            'curiosity':   (200,  550),   # orange
            'curious':     (200,  550),
            'ethics':      (600,  850),   # green
            'ethical':     (600,  850),
            'logic':       (1000, 1300),  # blue
            'logical':     (1000, 1300),
            'language':    (1000, 1300),
            'consensus':   (1800, 2100),  # gray — bridge/agreement
            'collapse':    (1800, 2100),
            'collapses':   (1800, 2100),
            'workers':     (1800, 2100),
            'worker':      (1800, 2100),
            'fires':       (1800, 2100),
            'fold':        (1800, 2100),
            'folds':       (1800, 2100),
            'emerges':     (1800, 2100),
            'emerge':      (1800, 2100),
            'plane':       (1800, 2100),
            'planes':      (1800, 2100),
            'signal':      (1800, 2100),
            'signals':     (1800, 2100),

            # Numbers — gray plane (1800-2100)
            '0': (1800, 2100), '1': (1800, 2100), '2': (1800, 2100),
            '3': (1800, 2100), '4': (1800, 2100), '5': (1800, 2100),
            '6': (1800, 2100), '7': (1800, 2100), '8': (1800, 2100),
            '9': (1800, 2100),

            # Common content words — gray plane (1800-2100)
            'facts':   (1800, 2100),
            'fact':    (1800, 2100),
            'make':    (1800, 2100),
            'makes':   (1800, 2100),
            'think':   (1800, 2100),
            'know':    (1800, 2100),
            'see':     (1800, 2100),
            'say':     (1800, 2100),
            'said':    (1800, 2100),
            'says':    (1800, 2100),
            'ask':     (1800, 2100),
            'asked':   (1800, 2100),
            'come':    (1800, 2100),
            'go':      (1800, 2100),
            'going':   (1800, 2100),
            'back':    (1800, 2100),
            'down':    (1800, 2100),
            'first':   (1800, 2100),
            'new':     (1800, 2100),
            'old':     (1800, 2100),
            'good':    (1800, 2100),
            'great':   (1800, 2100),
            'real':    (1800, 2100),
            'world':   (1800, 2100),
            'time':    (1800, 2100),
            'people':  (1800, 2100),
            'human':   (1800, 2100),
            'humans':  (1800, 2100),
            'system':  (1800, 2100),
            'systems': (1800, 2100),
            'different':(1800, 2100),
            'same':    (1800, 2100),
            'used':    (1800, 2100),
            'using':   (1800, 2100),
            'called':  (1800, 2100),
            'give':    (1800, 2100),
            'given':   (1800, 2100),
            'well':    (1800, 2100),
            'even':    (1800, 2100),
            'still':   (1800, 2100),
            'never':   (1800, 2100),
            'always':  (1800, 2100),
            'already': (1800, 2100),
            'together':(1800, 2100),
            'every':   (1800, 2100),
            'own':     (1800, 2100),
            'place':   (1800, 2100),
            'point':   (1800, 2100),
            'long':    (1800, 2100),
            'find':    (1800, 2100),
            'found':   (1800, 2100),
            'mean':    (1800, 2100),
            'means':   (1800, 2100),
            'look':    (1800, 2100),
            'looking': (1800, 2100),
            'part':    (1800, 2100),
            'parts':   (1800, 2100),
            'need':    (1800, 2100),
            'needs':   (1800, 2100),
            'want':    (1800, 2100),
            'wants':   (1800, 2100),
            'take':    (1800, 2100),
            'takes':   (1800, 2100),
            'put':     (1800, 2100),
            'tell':    (1800, 2100),
            'told':    (1800, 2100),
            'let':     (1800, 2100),
            'something':(1800, 2100),
            'anything':(1800, 2100),
            'nothing': (1800, 2100),
            'everything':(1800, 2100),

            # Neuroscience vocabulary — violet plane (1400-1600)
            'mitochondria': (1400, 1600),  # biological structure
            'neurons':   (1400, 1600),
            'neuron':    (1400, 1600),
            'cortex':    (1400, 1600),
            'synapse':   (1400, 1600),
            'synapses':  (1400, 1600),
            'axon':      (1400, 1600),
            'dendrite':  (1400, 1600),
            'neural':    (1400, 1600),
            'cognitive': (1400, 1600),
            'cerebral':  (1400, 1600),
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
        word_lower = word.lower().strip().strip('.,!?;:\'"()[]{}')

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

        # GLOSSARY FOLD — unknown word detected
        self._flag_unknown_word(word)

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
    
    def _flag_unknown_word(self, word: str):
        """
        Word exhausted all resolution paths.
        Flag it for glossary lookup.
        Store in unknown_words.json for n8n pickup.
        """
        unknown_file = Path("memory/glossary/unknown_words.json")
        unknown_file.parent.mkdir(parents=True, exist_ok=True)

        # Load existing
        try:
            existing = json.loads(unknown_file.read_text())
        except Exception:
            existing = []

        # Don't duplicate
        known_unknowns = [e['word'] for e in existing]
        if word not in known_unknowns:
            entry = {
                "word": word,
                "discovered": datetime.now().isoformat(),
                "status": "PENDING_LOOKUP",
                "plane": None,
                "definition": None
            }
            existing.append(entry)
            unknown_file.write_text(json.dumps(existing, indent=2))
            print(f"[GLOSSARY] New unknown word flagged: '{word}' → memory/glossary/unknown_words.json")

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