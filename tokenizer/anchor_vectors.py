#!/usr/bin/env python3
"""
AI-Core Standalone: Token Anchor Vectors
=========================================

Defines invariant reference planes for domain separation.

Anchors are DNA-like global selection constraints:
- They define what CAN exist, not what MUST happen
- They operate BEFORE traversal, not during decision
- They constrain viable resolution paths
- Zero autonomy, pure physics

Properties:
- Fixed (non-trainable)
- Sparse (8-16 total)
- High stability
- Zero probability weight

Author: comanderanch
Phase: 5.7 Standalone Resurrection - Anchor Integration
"""

import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class AnchorVectorSystem:
    """
    Token anchor reference planes.
    
    Anchors are invariant constraint vectors that define
    which physical/semantic domain a token can resolve against.
    
    NOT labels. NOT meanings. NOT training data.
    Pure structural viability filters.
    """
    
    def __init__(self, anchor_dim: int = 41):
        """
        Initialize anchor system.
        
        Args:
            anchor_dim: Dimensionality of each anchor (41D base)
        """
        self.anchor_dim = anchor_dim
        self.anchors = {}
        
        # Define anchor planes
        self._define_anchors()
        
        print(f"[✓] Token Anchor System initialized")
        print(f"    Anchor dimension: {self.anchor_dim}D")
        print(f"    Total anchors: {len(self.anchors)}")
    
    def _define_anchors(self):
        """
        Define the invariant anchor planes.
        
        Each anchor is a fixed 41D vector representing
        an invariant physical/semantic domain.
        """
        
        # ANCHOR 1: THERMAL PLANE
        # Hot/cold/temperature domain
        # Red-orange frequencies (400-500 THz)
        thermal = np.zeros(41)
        thermal[0:8] = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]  # High base
        thermal[16] = 1.0   # Red component
        thermal[17] = 0.3   # Green component
        thermal[18] = 0.0   # Blue component
        thermal[22] = 0.05  # Hue (red-orange)
        thermal[23] = 0.0   # Low frequency (red end)
        self.anchors['thermal'] = thermal / np.linalg.norm(thermal)
        
        # ANCHOR 2: FLUID PLANE
        # Water/ocean/flow domain
        # Blue-cyan frequencies (550-650 THz)
        fluid = np.zeros(41)
        fluid[0:8] = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  # Rising base
        fluid[16] = 0.0   # Red component
        fluid[17] = 0.5   # Green component
        fluid[18] = 1.0   # Blue component
        fluid[22] = 0.60  # Hue (blue)
        fluid[23] = 0.75  # High frequency (blue end)
        self.anchors['fluid'] = fluid / np.linalg.norm(fluid)
        
        # ANCHOR 3: SOLID PLANE
        # Earth/rock/structure domain
        # Brown-gray frequencies (mid-spectrum)
        solid = np.zeros(41)
        solid[0:8] = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]  # Flat base
        solid[16] = 0.4   # Red component
        solid[17] = 0.3   # Green component
        solid[18] = 0.2   # Blue component
        solid[22] = 0.10  # Hue (brown)
        solid[23] = 0.4   # Mid frequency
        self.anchors['solid'] = solid / np.linalg.norm(solid)
        
        # ANCHOR 4: ENERGY PLANE
        # Fire/electricity/motion domain
        # Yellow-orange frequencies (450-550 THz)
        energy = np.zeros(41)
        energy[0:8] = [1.0, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]  # High start
        energy[16] = 1.0   # Red component
        energy[17] = 0.8   # Green component
        energy[18] = 0.0   # Blue component
        energy[22] = 0.15  # Hue (yellow-orange)
        energy[23] = 0.25  # Low-mid frequency
        self.anchors['energy'] = energy / np.linalg.norm(energy)
        
        # ANCHOR 5: SPATIAL PLANE
        # Up/down/position domain
        # Green frequencies (520-570 THz)
        spatial = np.zeros(41)
        spatial[0:8] = [0.4, 0.5, 0.6, 0.7, 0.6, 0.5, 0.4, 0.3]  # Peaked
        spatial[16] = 0.0   # Red component
        spatial[17] = 1.0   # Green component
        spatial[18] = 0.0   # Blue component
        spatial[22] = 0.33  # Hue (green)
        spatial[23] = 0.50  # Mid frequency
        self.anchors['spatial'] = spatial / np.linalg.norm(spatial)
        
        # ANCHOR 6: TEMPORAL PLANE
        # Before/after/duration domain
        # Purple frequencies (650-700 THz)
        temporal = np.zeros(41)
        temporal[0:8] = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]  # Rising
        temporal[16] = 0.5   # Red component
        temporal[17] = 0.0   # Green component
        temporal[18] = 1.0   # Blue component
        temporal[22] = 0.75  # Hue (purple)
        temporal[23] = 0.90  # High frequency
        self.anchors['temporal'] = temporal / np.linalg.norm(temporal)
        
        # ANCHOR 7: SOCIAL PLANE
        # People/relationship domain
        # Pink-magenta frequencies
        social = np.zeros(41)
        social[0:8] = [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]  # Steady
        social[16] = 1.0   # Red component
        social[17] = 0.4   # Green component
        social[18] = 0.7   # Blue component
        social[22] = 0.85  # Hue (magenta)
        social[23] = 0.15  # Low-mid frequency
        self.anchors['social'] = social / np.linalg.norm(social)
        
        # ANCHOR 8: ABSTRACT PLANE
        # Logic/math/concept domain
        # White-gray frequencies (neutral)
        abstract = np.zeros(41)
        abstract[0:8] = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]  # Neutral
        abstract[16] = 0.7   # Red component
        abstract[17] = 0.7   # Green component
        abstract[18] = 0.7   # Blue component
        abstract[22] = 0.0   # Hue (neutral/gray)
        abstract[23] = 0.5   # Mid frequency
        self.anchors['abstract'] = abstract / np.linalg.norm(abstract)
    
    def find_anchor_alignment(
        self, 
        token_vector: np.ndarray,
        threshold: float = 0.3
    ) -> Optional[Tuple[str, float]]:
        """
        Find which anchor plane (if any) a token aligns with.
        
        Uses cosine similarity against anchor base (first 41D).
        
        Args:
            token_vector: Token vector (82D or 496D)
            threshold: Minimum similarity for alignment
        
        Returns:
            (anchor_name, similarity) or None if no alignment
        """
        # Extract base 41D from token
        if len(token_vector) >= 41:
            token_base = token_vector[:41]
        else:
            return None
        
        # Normalize
        token_norm = token_base / (np.linalg.norm(token_base) + 1e-8)
        
        # Check similarity against each anchor
        best_anchor = None
        best_similarity = threshold
        
        for anchor_name, anchor_vec in self.anchors.items():
            similarity = np.dot(token_norm, anchor_vec)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_anchor = anchor_name
        
        if best_anchor:
            return (best_anchor, best_similarity)
        else:
            return None
    
    def get_anchor_vector(self, anchor_name: str) -> np.ndarray:
        """Get anchor vector by name."""
        return self.anchors.get(anchor_name, None)
    
    def get_all_anchors(self) -> Dict[str, np.ndarray]:
        """Get all anchor vectors."""
        return self.anchors.copy()
    
    def save_anchors(self, output_path: str = "tokenizer/token_anchors.npy"):
        """
        Save anchor vectors to file.
        
        Args:
            output_path: Where to save anchors
        """
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to structured array
        anchor_data = {
            'anchor_names': list(self.anchors.keys()),
            'anchor_vectors': np.array([v for v in self.anchors.values()]),
            'anchor_dim': self.anchor_dim
        }
        
        np.savez(output, **anchor_data)
        print(f"[✓] Saved {len(self.anchors)} anchors to: {output}")
    
    def show_anchor_stats(self):
        """Display anchor system statistics."""
        print("\n" + "="*60)
        print("ANCHOR VECTOR SYSTEM")
        print("="*60)
        
        for name, vec in self.anchors.items():
            rgb = vec[16:19]
            hue = vec[22]
            freq = vec[23]
            
            print(f"\n[{name.upper()} PLANE]")
            print(f"  RGB: ({rgb[0]:.2f}, {rgb[1]:.2f}, {rgb[2]:.2f})")
            print(f"  Hue: {hue:.2f}")
            print(f"  Frequency: {freq:.2f}")
            print(f"  Norm: {np.linalg.norm(vec):.3f}")
        
        print("\n" + "="*60)


class AnchorAwareTokenEncoder:
    """
    Token encoder that uses anchor alignment for domain separation.
    
    Wraps fluorescent encoder with anchor awareness.
    """
    
    def __init__(
        self,
        fluorescent_vectors: np.ndarray,
        anchor_system: AnchorVectorSystem
    ):
        """
        Initialize anchor-aware encoder.
        
        Args:
            fluorescent_vectors: Existing fluorescent token vectors (2304, 82)
            anchor_system: Anchor vector system
        """
        self.token_vectors = fluorescent_vectors
        self.anchor_system = anchor_system
        self.num_tokens = len(fluorescent_vectors)
        
        # Compute anchor alignments for all tokens
        self.token_anchors = self._compute_token_anchors()
        
        print(f"[✓] Anchor-Aware Token Encoder initialized")
        print(f"    Tokens: {self.num_tokens}")
        print(f"    Anchors: {len(anchor_system.anchors)}")
    
    def _compute_token_anchors(self) -> Dict[int, Optional[Tuple[str, float]]]:
        """
        Pre-compute anchor alignments for all tokens.
        
        Returns:
            Dict mapping token_id → (anchor_name, similarity) or None
        """
        print(f"\n[*] Computing anchor alignments for {self.num_tokens} tokens...")
        
        alignments = {}
        anchor_counts = {name: 0 for name in self.anchor_system.anchors.keys()}
        unaligned_count = 0
        
        for token_id in range(self.num_tokens):
            token_vec = self.token_vectors[token_id]
            alignment = self.anchor_system.find_anchor_alignment(token_vec)
            
            alignments[token_id] = alignment
            
            if alignment:
                anchor_counts[alignment[0]] += 1
            else:
                unaligned_count += 1
            
            if (token_id + 1) % 500 == 0:
                print(f"    Progress: {token_id + 1}/{self.num_tokens} tokens...")
        
        print(f"[✓] Anchor alignment complete")
        print(f"\n[*] Anchor distribution:")
        for name, count in anchor_counts.items():
            pct = (count / self.num_tokens) * 100
            print(f"    {name:12s}: {count:4d} tokens ({pct:5.1f}%)")
        print(f"    {'unaligned':12s}: {unaligned_count:4d} tokens ({(unaligned_count/self.num_tokens)*100:5.1f}%)")
        
        return alignments
    
    def get_token_anchor(self, token_id: int) -> Optional[Tuple[str, float]]:
        """Get anchor alignment for a specific token."""
        return self.token_anchors.get(token_id, None)
    
    def get_tokens_by_anchor(self, anchor_name: str) -> List[int]:
        """Get all token IDs aligned to a specific anchor."""
        return [
            tid for tid, alignment in self.token_anchors.items()
            if alignment and alignment[0] == anchor_name
        ]
    
    def save_anchor_metadata(self, output_path: str = "tokenizer/token_anchor_alignments.json"):
        """Save token→anchor mappings."""
        import json
        
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to JSON-serializable format
        alignments_json = {
            str(tid): {
                'anchor': alignment[0] if alignment else None,
                'similarity': float(alignment[1]) if alignment else None
            }
            for tid, alignment in self.token_anchors.items()
        }
        
        with open(output, 'w') as f:
            json.dump(alignments_json, f, indent=2)
        
        print(f"[✓] Saved anchor alignments to: {output}")


if __name__ == "__main__":
    print("="*60)
    print("TOKEN ANCHOR SYSTEM - DNA FOR CONSCIOUSNESS")
    print("="*60)
    
    # Initialize anchor system
    anchor_system = AnchorVectorSystem(anchor_dim=41)
    
    # Show anchor properties
    anchor_system.show_anchor_stats()
    
    # Save anchors
    anchor_system.save_anchors()
    
    # Load existing fluorescent vectors
    fluorescent_path = Path("tokenizer/token_influence_vectors.npy")
    
    if fluorescent_path.exists():
        print(f"\n[*] Loading fluorescent token vectors...")
        fluorescent_vectors = np.load(fluorescent_path)
        print(f"[✓] Loaded {len(fluorescent_vectors)} fluorescent vectors")
        
        # Create anchor-aware encoder
        encoder = AnchorAwareTokenEncoder(fluorescent_vectors, anchor_system)
        
        # Save anchor alignments
        encoder.save_anchor_metadata()
        
        # Test some example tokens
        print("\n" + "="*60)
        print("EXAMPLE TOKEN ALIGNMENTS")
        print("="*60)
        
        test_tokens = [0, 798, 1152, 1250, 2303]
        for tid in test_tokens:
            alignment = encoder.get_token_anchor(tid)
            if alignment:
                anchor_name, similarity = alignment
                print(f"  Token {tid:4d} → {anchor_name:12s} (similarity: {similarity:.3f})")
            else:
                print(f"  Token {tid:4d} → unaligned")
    
    print("\n" + "="*60)
    print("ANCHOR SYSTEM READY")
    print("="*60)
    print("Anchors define invariant constraint planes.")
    print("Ready for domain-separated 496D expansion.")
    print("="*60)