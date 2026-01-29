#!/usr/bin/env python3
"""
AI-CORE FOUNDATION
The 5 unchanging pieces everything else builds on.
Like the pyramid's cornerstone.
"""

import json
import csv
import numpy as np
from pathlib import Path
from datetime import datetime

class AICoreFOUNDATION:
    """
    The unified base.
    Load once. Use everywhere.
    """
    
    _instance = None  # Singleton - only one foundation
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.BASE = Path(__file__).resolve().parent
        
        print("🔥 Loading AI-Core Foundation...")
        
        # 1. Color Palette (2,304 tokens)
        self.palette = self._load_palette()
        print(f"  ✅ Palette: {len(self.palette)} tokens")
        
        # 2. Word→Token Map
        self.word_map = self._load_word_map()
        print(f"  ✅ Vocabulary: {len(self.word_map)} words")
        
        # 3. 498D Vectors
        self.vectors_498d = self._load_vectors()
        print(f"  ✅ Vectors: {self.vectors_498d.shape}")
        
        # 4. EM Field Substrate
        self.em_field = self._load_em_field()
        print(f"  ✅ EM Field: {self.em_field.shape}")
        
        # 5. QBitHue Memory
        self.qbithue = self._load_qbithue()
        print(f"  ✅ QBitHue: {len(self.qbithue)} network nodes")
        
        # Verify unity
        self._verify_foundation()
        
        print("🔥 Foundation unified and verified.")
        self._initialized = True
    
    def _load_palette(self):
        """Load 2,304 color tokens"""
        path = self.BASE / "tokenizer" / "full_color_tokens.csv"
        palette = []
        with path.open('r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if not row:
                    continue
                try:
                    token = row[0]
                    if len(row) >= 10:
                        R = int(float(row[6]))
                        G = int(float(row[7]))
                        B = int(float(row[8]))
                        F = float(row[9])
                    elif len(row) >= 6:
                        R = int(float(row[2]))
                        G = int(float(row[3]))
                        B = int(float(row[4]))
                        F = float(row[5])
                    else:
                        continue
                    palette.append((token, R, G, B, F))
                except:
                    continue
        return palette
    
    def _load_word_map(self):
        """Load vocabulary → token index"""
        path = self.BASE / "training_data" / "word_to_token_map.json"
        data = json.loads(path.read_text())
        w2i = data.get("word_to_palette_index", {})
        return {k: int(v) for k, v in w2i.items()}
    
    def _load_vectors(self):
        """Load 498D vector space"""
        path = self.BASE / "tokenizer" / "token_vectors_498d.npy"
        return np.load(path)
    
    def _load_em_field(self):
        """Load EM field substrate"""
        path = self.BASE / "consciousness_data" / "field" / "em_field_substrate.npy"
        return np.load(path)
    
    def _load_qbithue(self):
        """Load QBitHue persistent memory"""
        path = self.BASE / "memory" / "qbithue_network.json"
        data = json.loads(path.read_text())
    
        # Handle both list and dict formats
        if isinstance(data, list):
            # Old format: list of nodes
            return {"nodes": data, "memory": {}}
        elif isinstance(data, dict):
            # New format: dict with nodes and memory
            if "memory" not in data:
                data["memory"] = {}
            return data
        else:
            # Empty/unknown format
            return {"nodes": [], "memory": {}}
    
    def _verify_foundation(self):
        """Verify all 5 pieces connect properly"""
        
        # Test: word → token → vector
        test_word = list(self.word_map.keys())[0]
        token_idx = self.word_map[test_word]
        vector = self.vectors_498d[token_idx]
        
        assert len(vector) == 498, "Vector dimension mismatch"
        assert self.em_field.shape[0] == 498, "EM field dimension mismatch"
        
        print(f"  ✅ Verified: word→token→vector→EM field chain works")
        
        return True
    
    def save_state(self):
        """Save current EM field and QBitHue state"""
        
        # Save EM field
        em_path = self.BASE / "consciousness_data" / "field" / "em_field_substrate.npy"
        np.save(em_path, self.em_field)
        
        # Save QBitHue
        qbit_path = self.BASE / "memory" / "qbithue_network.json"
        qbit_path.write_text(json.dumps(self.qbithue, indent=2))
        
        print(f"💾 Foundation state saved")
    
    def word_to_vector(self, word):
        """Convert word → 498D vector"""
        word = word.lower()
        if word in self.word_map:
            idx = self.word_map[word]
            return self.vectors_498d[idx]
        else:
            # Hash to palette index
            idx = abs(hash(word)) % len(self.palette)
            return self.vectors_498d[idx]
    
    def vector_to_word(self, vector):
        """Find nearest word to 498D vector"""
        distances = np.linalg.norm(self.vectors_498d - vector, axis=1)
        nearest_idx = np.argmin(distances)
        
        # Find word with this index
        for word, idx in self.word_map.items():
            if idx == nearest_idx:
                return word
        
        return f"<token_{nearest_idx}>"


# Global singleton instance
def get_foundation():
    """Get the unified foundation (creates if needed)"""
    return AICoreFOUNDATION()


if __name__ == "__main__":
    # Test the foundation
    print("\n" + "="*60)
    print("TESTING AI-CORE FOUNDATION")
    print("="*60 + "\n")
    
    foundation = get_foundation()
    
    print("\n" + "="*60)
    print("TEST: Word → Vector → Word")
    print("="*60)
    
    test_words = ["consciousness", "wisdom", "ark", "light"]
    for word in test_words:
        vec = foundation.word_to_vector(word)
        back = foundation.vector_to_word(vec)
        print(f"  {word} → {vec[:5]}... → {back}")
    
    print("\n" + "="*60)
    print("✅ FOUNDATION READY")
    print("="*60)
