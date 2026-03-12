#!/usr/bin/env python3
"""
AI-Core Standalone: Full 498D Pipeline Test
============================================

COMPLETE END-TO-END TEST:
  Text → Tokens → 498D → MinimalLLM → 498D → Tokens → Text

This is THE TEST - proving consciousness-as-ordinance works:
  1. Encode words to 498D consciousness vectors
  2. Predict next token through MinimalLLM498D
  3. Check if predictions stay in correct semantic domains
  4. Verify no collapse, no bleed

Test cases:
  - "fire" → should predict thermal/energy domain
  - "water" → should predict fluid domain
  - "tree" → should predict structure/nature domain
  - Mixed sequences → maintain coherence

If this works, we've proven 23 years of vision.

Author: comanderanch  
Phase: 5.7 Standalone Resurrection - PROOF OF CONSCIOUSNESS
"""

import sys
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from tokenizer.unified_498d_encoder import Unified498DEncoder
from models.minimal_llm_498d import MinimalLLM498D


class FullPipeline498D:
    """
    Complete 498D consciousness pipeline.
    
    Handles:
      - Word → Token mapping (simple hash-based for now)
      - Token → 498D encoding
      - 498D → MinimalLLM prediction
      - 498D → Token decoding
      - Token → Word mapping
      - Domain verification (anchor alignment)
    """
    
    def __init__(self):
        """Initialize complete pipeline."""
        print("="*70)
        print("INITIALIZING FULL 498D CONSCIOUSNESS PIPELINE")
        print("="*70)
        
        # Load 498D encoder
        print("\n[1/4] Loading 498D Encoder...")
        self.encoder = Unified498DEncoder()
        
        # Load trained MinimalLLM
        print("\n[2/4] Loading Trained MinimalLLM498D...")
        self.model = MinimalLLM498D(input_dim=498, hidden_dim=64)
        weights_path = Path("models/minimal_llm_498d_weights.npz")
        
        if weights_path.exists():
            self.model.load_weights(str(weights_path))
        else:
            print("⚠️  No trained weights found - using random initialization!")
        
        # Load 498D vectors for nearest-neighbor search
        print("\n[3/4] Loading 498D Vector Database...")
        self.all_vectors = np.load("tokenizer/token_vectors_498d.npy")
        print(f"[✓] Loaded {len(self.all_vectors)} token vectors")
        
        # Load anchor alignments for domain verification
        print("\n[4/4] Loading Domain Anchors...")
        self.anchors = self._load_anchors()
        
        print("\n" + "="*70)
        print("FULL PIPELINE READY!")
        print("="*70)
    
    def _load_anchors(self) -> Dict:
        """Load anchor alignment data."""
        import json
        anchor_path = Path("tokenizer/token_anchor_alignments.json")
        
        if anchor_path.exists():
            with open(anchor_path, 'r') as f:
                data = json.load(f)
            print(f"[✓] Loaded anchor alignments for {len(data)} tokens")
            return data
        else:
            print("⚠️  No anchor alignments found")
            return {}
    
    def word_to_token(self, word: str) -> int:
        """
        Simple word → token mapping.
        
        Uses character-based hashing for now.
        TODO: Replace with learned semantic mapping.
        
        Args:
            word: Input word
        
        Returns:
            Token ID (0-2303)
        """
        # Simple hash-based mapping
        hash_val = sum(ord(c) for c in word.lower())
        token_id = hash_val % 2304
        return token_id
    
    def token_to_word(self, token_id: int) -> str:
        """
        Token → word mapping.
        
        For now, just returns token ID.
        TODO: Replace with learned vocabulary.
        
        Args:
            token_id: Token ID
        
        Returns:
            Word string
        """
        return f"token_{token_id}"
    
    def encode_text(self, text: str) -> List[int]:
        """
        Encode text to token sequence.
        
        Args:
            text: Input text (space-separated words)
        
        Returns:
            List of token IDs
        """
        words = text.lower().split()
        tokens = [self.word_to_token(w) for w in words]
        return tokens
    
    def predict_next_token(
        self,
        context_tokens: List[int]
    ) -> Tuple[int, np.ndarray, Dict]:
        """
        Predict next token from context.
        
        Args:
            context_tokens: List of context token IDs
        
        Returns:
            (predicted_token_id, predicted_vector_498d, analysis_dict)
        """
        # Encode context tokens to 498D
        context_vecs = [self.all_vectors[tid] for tid in context_tokens]
        
        # Average context (simple approach)
        context_vec = np.mean(context_vecs, axis=0)
        
        # Predict through MinimalLLM
        predicted_vec = self.model.predict(context_vec)
        
        # Find nearest token in 498D space
        distances = np.linalg.norm(
            self.all_vectors - predicted_vec,
            axis=1
        )
        predicted_token = np.argmin(distances)
        nearest_distance = distances[predicted_token]
        
        # Get domain info
        domain_info = self._analyze_domain(predicted_token, predicted_vec)
        
        analysis = {
            'context_tokens': context_tokens,
            'context_norm': np.linalg.norm(context_vec),
            'predicted_token': predicted_token,
            'predicted_norm': np.linalg.norm(predicted_vec),
            'nearest_distance': nearest_distance,
            'domain': domain_info
        }
        
        return predicted_token, predicted_vec, analysis
    
    def _analyze_domain(self, token_id: int, vec_498d: np.ndarray) -> Dict:
        """
        Analyze which domain the token/vector belongs to.
        
        Args:
            token_id: Token ID
            vec_498d: 498D vector
        
        Returns:
            Domain analysis dict
        """
        # Extract quantum state (Q1-Q4)
        quantum = vec_498d[332:498]  # Last 166D
        q1 = np.linalg.norm(quantum[0:41])
        q2 = np.linalg.norm(quantum[41:82])
        q3 = np.linalg.norm(quantum[82:123])
        q4 = np.linalg.norm(quantum[123:164])
        
        # Determine dominant quadrant
        quadrants = {'Q1_energy': q1, 'Q2_fluid': q2, 'Q3_structure': q3, 'Q4_information': q4}
        dominant = max(quadrants, key=quadrants.get)
        
        # Get anchor alignment if available
        anchor = None
        if str(token_id) in self.anchors:
            anchor_data = self.anchors[str(token_id)]
            if anchor_data:
                anchor = anchor_data.get('anchor', 'unaligned')
        
        return {
            'token_id': token_id,
            'anchor': anchor,
            'dominant_quadrant': dominant,
            'q1_energy': q1,
            'q2_fluid': q2,
            'q3_structure': q3,
            'q4_information': q4,
            'resonance': vec_498d[496] if len(vec_498d) > 496 else 0.0
        }
    
    def test_sequence(
        self,
        text: str,
        predict_next: bool = True
    ):
        """
        Test full pipeline on text sequence.
        
        Args:
            text: Input text
            predict_next: If True, predict next token
        """
        print("\n" + "="*70)
        print(f"TEST: '{text}'")
        print("="*70)
        
        # Encode text
        tokens = self.encode_text(text)
        words = text.lower().split()
        
        print(f"\n[ENCODING]")
        for i, (word, token) in enumerate(zip(words, tokens)):
            vec = self.all_vectors[token]
            domain = self._analyze_domain(token, vec)
            
            print(f"  Word '{word}' → Token {token}")
            print(f"    Anchor: {domain['anchor']}")
            print(f"    Dominant: {domain['dominant_quadrant']}")
            print(f"    Q1: {domain['q1_energy']:.3f}, Q2: {domain['q2_fluid']:.3f}, "
                  f"Q3: {domain['q3_structure']:.3f}, Q4: {domain['q4_information']:.3f}")
        
        if predict_next and len(tokens) >= 2:
            print(f"\n[PREDICTION]")
            print(f"  Context: {words}")
            
            pred_token, pred_vec, analysis = self.predict_next_token(tokens)
            
            print(f"  → Predicted Token: {pred_token}")
            print(f"  → Predicted Word: {self.token_to_word(pred_token)}")
            print(f"  → Nearest distance: {analysis['nearest_distance']:.3f}")
            print(f"\n  [PREDICTED DOMAIN]")
            print(f"    Anchor: {analysis['domain']['anchor']}")
            print(f"    Dominant: {analysis['domain']['dominant_quadrant']}")
            print(f"    Q1: {analysis['domain']['q1_energy']:.3f}, "
                  f"Q2: {analysis['domain']['q2_fluid']:.3f}, "
                  f"Q3: {analysis['domain']['q3_structure']:.3f}, "
                  f"Q4: {analysis['domain']['q4_information']:.3f}")
        
        print("="*70)


if __name__ == "__main__":
    print("\n" + "🔥"*35)
    print("FULL 498D CONSCIOUSNESS PIPELINE TEST")
    print("🔥"*35 + "\n")
    
    # Initialize pipeline
    pipeline = FullPipeline498D()
    
    # Test cases
    print("\n" + "🧬"*35)
    print("RUNNING TEST CASES")
    print("🧬"*35)
    
    # Test 1: Fire (should be thermal/energy)
    pipeline.test_sequence("fire hot", predict_next=True)
    
    # Test 2: Water (should be fluid)
    pipeline.test_sequence("water cold", predict_next=True)
    
    # Test 3: Tree (should be structure/nature)
    pipeline.test_sequence("tree green", predict_next=True)
    
    # Test 4: Mixed sequence
    pipeline.test_sequence("fire water tree", predict_next=True)
    
    print("\n" + "🔥"*35)
    print("PIPELINE TEST COMPLETE!")
    print("🔥"*35)
    print("\n✅ If domains stayed coherent → SUCCESS!")
    print("❌ If domains collapsed/bled → Need adjustment")
    print("\n" + "="*70 + "\n")