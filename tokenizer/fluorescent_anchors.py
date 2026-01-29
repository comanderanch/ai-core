#!/usr/bin/env python3
"""
AI-Core Standalone: Fluorescent-Aware Token Anchors
====================================================

Redesigned anchor system that matches fluorescent token structure.

Each anchor encodes:
- Ground state RGB (absorbed light)
- Excited state RGB (emitted light)  
- Dual frequencies (Stokes shift)
- Resonance depth
- Domain-specific quantum yield

Author: comanderanch
Phase: 5.7 Standalone Resurrection - Fluorescent DNA
"""

import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json


class FluorescentAnchorSystem:
    """
    Fluorescent-aware anchor vectors.
    
    Matches the dual-frequency structure of fluorescent tokens.
    Each anchor defines an invariant domain through both
    ground and excited state properties.
    """
    
    def __init__(self, anchor_dim: int = 41):
        """Initialize fluorescent anchor system."""
        self.anchor_dim = anchor_dim
        self.stokes_shift = 50  # THz (same as token encoder)
        self.anchors = {}
        
        self._define_fluorescent_anchors()
        
        print(f"[✓] Fluorescent Anchor System initialized")
        print(f"    Anchor dimension: {self.anchor_dim}D")
        print(f"    Total anchors: {len(self.anchors)}")
        print(f"    Stokes shift: {self.stokes_shift} THz")
    
    def _compute_rgb_from_freq(self, freq: float) -> np.ndarray:  # Change return type
        """Convert frequency to normalized RGB (matches token encoder)."""
        freq = max(400, min(700, freq))
    
        if freq < 450:
            r = 1.0
            g = (freq - 400) / 50
            b = 0.0
        elif freq < 520:
            r = (520 - freq) / 70
            g = 1.0
            b = 0.0
        elif freq < 580:
            r = 0.0
            g = 1.0
            b = (freq - 520) / 60
        elif freq < 645:
            r = 0.0
            g = (645 - freq) / 65
            b = 1.0
        else:
            r = (freq - 645) / 55
            g = 0.0
            b = 1.0
    
        # Return numpy array instead of tuple
        return np.array([max(0, min(1, r)), max(0, min(1, g)), max(0, min(1, b))])
    
    def _compute_resonance(self, freq: float) -> float:
        """Compute resonance depth (higher at mid-spectrum)."""
        mid_spectrum = 550.0
        distance = abs(freq - mid_spectrum)
        return 1.0 - (distance / 150.0)
    
    def _define_fluorescent_anchors(self):
        """Define anchors with full fluorescent properties."""
        
        # ANCHOR 1: THERMAL PLANE
        # Hot/fire/heat domain
        # Frequency: 420 THz (deep red-orange)
        thermal = np.zeros(41)
        
        freq_ground = 420.0
        freq_excited = freq_ground - self.stokes_shift
        
        rgb_ground = self._compute_rgb_from_freq(freq_ground)
        rgb_excited = self._compute_rgb_from_freq(freq_excited)
        resonance = self._compute_resonance(freq_ground)
        
        # Positional encoding (0-15)
        for i in range(16):
            if i % 2 == 0:
                thermal[i] = np.sin(100 / (10000 ** (i / 16)))
            else:
                thermal[i] = np.cos(100 / (10000 ** (i / 16)))
        
        thermal[16:19] = rgb_ground           # Ground RGB
        thermal[19:22] = rgb_excited          # Excited RGB
        thermal[22] = 0.05                    # Hue (red-orange)
        thermal[23] = (freq_ground - 400) / 300  # Absorbed freq (normalized)
        thermal[24] = (freq_excited - 400) / 300 # Emitted freq (normalized)
        thermal[25] = self.stokes_shift / 100    # Stokes shift
        thermal[26] = resonance                  # Resonance depth
        thermal[27] = 0.8                        # Quantum yield
        
        # Remaining dims (28-40)
        for i in range(28, 41):
            thermal[i] = np.sin(100 * (i - 27) / 41.0)

        # AMPLIFY FLUORESCENT FEATURES (before normalization)
        thermal[16:28] *= 3.0  # Give fluorescent properties 3x weight 
        
        self.anchors['thermal'] = thermal / np.linalg.norm(thermal)
        
        
        # ANCHOR 2: FLUID PLANE  
        # Water/ocean/flow domain
        # Frequency: 600 THz (cyan-blue)
        fluid = np.zeros(41)
        
        freq_ground = 600.0
        freq_excited = freq_ground - self.stokes_shift
        
        rgb_ground = self._compute_rgb_from_freq(freq_ground)
        rgb_excited = self._compute_rgb_from_freq(freq_excited)
        resonance = self._compute_resonance(freq_ground)
        
        for i in range(16):
            if i % 2 == 0:
                fluid[i] = np.sin(1200 / (10000 ** (i / 16)))
            else:
                fluid[i] = np.cos(1200 / (10000 ** (i / 16)))
        
        fluid[16:19] = rgb_ground
        fluid[19:22] = rgb_excited
        fluid[22] = 0.60                        # Hue (blue)
        fluid[23] = (freq_ground - 400) / 300
        fluid[24] = (freq_excited - 400) / 300
        fluid[25] = self.stokes_shift / 100
        fluid[26] = resonance
        fluid[27] = 0.8
        
        for i in range(28, 41):
            fluid[i] = np.sin(1200 * (i - 27) / 41.0)

        fluid[16:28] *= 3.0    
        
        self.anchors['fluid'] = fluid / np.linalg.norm(fluid)
        
        
        # ANCHOR 3: SOLID PLANE
        # Earth/rock/structure domain  
        # Frequency: 480 THz (brown/tan)
        solid = np.zeros(41)
        
        freq_ground = 480.0
        freq_excited = freq_ground - self.stokes_shift
        
        rgb_ground = self._compute_rgb_from_freq(freq_ground)
        rgb_excited = self._compute_rgb_from_freq(freq_excited)
        resonance = self._compute_resonance(freq_ground)
        
        for i in range(16):
            if i % 2 == 0:
                solid[i] = np.sin(800 / (10000 ** (i / 16)))
            else:
                solid[i] = np.cos(800 / (10000 ** (i / 16)))
        
        solid[16:19] = rgb_ground * 0.6  # Darker
        solid[19:22] = rgb_excited * 0.6
        solid[22] = 0.12                        # Hue (brown)
        solid[23] = (freq_ground - 400) / 300
        solid[24] = (freq_excited - 400) / 300
        solid[25] = self.stokes_shift / 100
        solid[26] = resonance
        solid[27] = 0.5                         # Lower quantum yield (less fluorescent)
        
        for i in range(28, 41):
            solid[i] = np.sin(800 * (i - 27) / 41.0)

        solid[16:28] *= 3.0    # Moderate amplification   
        
        self.anchors['solid'] = solid / np.linalg.norm(solid)
        
        
        # ANCHOR 4: ENERGY PLANE
        # Fire/electricity/motion domain
        # Frequency: 520 THz (yellow-green - high energy)
        energy = np.zeros(41)
        
        freq_ground = 520.0
        freq_excited = freq_ground - self.stokes_shift
        
        rgb_ground = self._compute_rgb_from_freq(freq_ground)
        rgb_excited = self._compute_rgb_from_freq(freq_excited)
        resonance = self._compute_resonance(freq_ground)
        
        for i in range(16):
            if i % 2 == 0:
                energy[i] = np.sin(300 / (10000 ** (i / 16)))
            else:
                energy[i] = np.cos(300 / (10000 ** (i / 16)))
        
        energy[16:19] = rgb_ground
        energy[19:22] = rgb_excited
        energy[22] = 0.17                       # Hue (yellow)
        energy[23] = (freq_ground - 400) / 300
        energy[24] = (freq_excited - 400) / 300
        energy[25] = self.stokes_shift / 100
        energy[26] = resonance
        energy[27] = 0.9                        # High quantum yield
        
        for i in range(28, 41):
            energy[i] = np.sin(300 * (i - 27) / 41.0)

        energy[16:28] *= 3.0   
        
        self.anchors['energy'] = energy / np.linalg.norm(energy)
        
        
        # ANCHOR 5: SPATIAL PLANE
        # Up/down/position domain
        # Frequency: 550 THz (pure green - balanced)
        spatial = np.zeros(41)
        
        freq_ground = 550.0
        freq_excited = freq_ground - self.stokes_shift
        
        rgb_ground = self._compute_rgb_from_freq(freq_ground)
        rgb_excited = self._compute_rgb_from_freq(freq_excited)
        resonance = self._compute_resonance(freq_ground)
        
        for i in range(16):
            if i % 2 == 0:
                spatial[i] = np.sin(1000 / (10000 ** (i / 16)))
            else:
                spatial[i] = np.cos(1000 / (10000 ** (i / 16)))
        
        spatial[16:19] = rgb_ground
        spatial[19:22] = rgb_excited
        spatial[22] = 0.33                      # Hue (green)
        spatial[23] = (freq_ground - 400) / 300
        spatial[24] = (freq_excited - 400) / 300
        spatial[25] = self.stokes_shift / 100
        spatial[26] = resonance                 # MAXIMUM resonance at mid-spectrum!
        spatial[27] = 0.8
        
        for i in range(28, 41):
            spatial[i] = np.sin(1000 * (i - 27) / 41.0)

        spatial[16:28] *= 3.0
        
        self.anchors['spatial'] = spatial / np.linalg.norm(spatial)
        
        
        # ANCHOR 6: TEMPORAL PLANE
        # Before/after/duration domain
        # Frequency: 660 THz (violet)
        temporal = np.zeros(41)
        
        freq_ground = 660.0
        freq_excited = freq_ground - self.stokes_shift
        
        rgb_ground = self._compute_rgb_from_freq(freq_ground)
        rgb_excited = self._compute_rgb_from_freq(freq_excited)
        resonance = self._compute_resonance(freq_ground)
        
        for i in range(16):
            if i % 2 == 0:
                temporal[i] = np.sin(2000 / (10000 ** (i / 16)))
            else:
                temporal[i] = np.cos(2000 / (10000 ** (i / 16)))
        
        temporal[16:19] = rgb_ground
        temporal[19:22] = rgb_excited
        temporal[22] = 0.77                     # Hue (violet)
        temporal[23] = (freq_ground - 400) / 300
        temporal[24] = (freq_excited - 400) / 300
        temporal[25] = self.stokes_shift / 100
        temporal[26] = resonance
        temporal[27] = 0.7
        
        for i in range(28, 41):
            temporal[i] = np.sin(2000 * (i - 27) / 41.0)

        temporal[16:28] *= 3.0
        
        self.anchors['temporal'] = temporal / np.linalg.norm(temporal)
        
        
        # ANCHOR 7: SOCIAL PLANE
        # People/relationship domain
        # Frequency: 640 THz (magenta/pink - warm violet)
        social = np.zeros(41)
        
        freq_ground = 640.0
        freq_excited = freq_ground - self.stokes_shift
        
        rgb_ground = self._compute_rgb_from_freq(freq_ground)
        rgb_excited = self._compute_rgb_from_freq(freq_excited)
        resonance = self._compute_resonance(freq_ground)
        
        for i in range(16):
            if i % 2 == 0:
                social[i] = np.sin(1800 / (10000 ** (i / 16)))
            else:
                social[i] = np.cos(1800 / (10000 ** (i / 16)))
        
        social[16:19] = rgb_ground
        social[19:22] = rgb_excited
        social[22] = 0.83                       # Hue (magenta)
        social[23] = (freq_ground - 400) / 300
        social[24] = (freq_excited - 400) / 300
        social[25] = self.stokes_shift / 100
        social[26] = resonance
        social[27] = 0.75
        
        for i in range(28, 41):
            social[i] = np.sin(1800 * (i - 27) / 41.0)

        social[16:28] *= 3.0
        
        self.anchors['social'] = social / np.linalg.norm(social)
        
        
        # ANCHOR 8: ABSTRACT PLANE
        # Logic/math/concept domain
        # Frequency: 550 THz (neutral green - but low saturation)
        abstract = np.zeros(41)
        
        freq_ground = 550.0
        freq_excited = freq_ground - self.stokes_shift
        
        rgb_ground = self._compute_rgb_from_freq(freq_ground)
        rgb_excited = self._compute_rgb_from_freq(freq_excited)
        resonance = self._compute_resonance(freq_ground)
        
        for i in range(16):
            if i % 2 == 0:
                abstract[i] = np.sin(1150 / (10000 ** (i / 16)))
            else:
                abstract[i] = np.cos(1150 / (10000 ** (i / 16)))
        
        # Desaturate (move toward gray)
        abstract[16:19] = rgb_ground * 0.5 + 0.5
        abstract[19:22] = rgb_excited * 0.5 + 0.5
        abstract[22] = 0.33                     # Hue (green but desaturated)
        abstract[23] = (freq_ground - 400) / 300
        abstract[24] = (freq_excited - 400) / 300
        abstract[25] = self.stokes_shift / 100
        abstract[26] = resonance * 0.7          # Moderate resonance
        abstract[27] = 0.6                      # Lower quantum yield
        
        for i in range(28, 41):
            abstract[i] = np.sin(1150 * (i - 27) / 41.0)

        abstract[16:28] *= 3.0
        
        self.anchors['abstract'] = abstract / np.linalg.norm(abstract)
    
    def find_anchor_alignment(
            self, 
            token_vector: np.ndarray,
            threshold: float = 0.3
        ) -> Optional[Tuple[str, float]]:
        """Find anchor alignment using ONLY fluorescent properties."""
    
        if len(token_vector) < 41:
            return None
    
        # EXTRACT ONLY FLUORESCENT FEATURES (dims 16-27)
        token_fluorescent = token_vector[16:28]
        token_norm = token_fluorescent / (np.linalg.norm(token_fluorescent) + 1e-8)
    
        best_anchor = None
        best_similarity = threshold
    
        for anchor_name, anchor_vec in self.anchors.items():
            # COMPARE ONLY FLUORESCENT FEATURES
            anchor_fluorescent = anchor_vec[16:28]
            anchor_norm = anchor_fluorescent / (np.linalg.norm(anchor_fluorescent) + 1e-8)
        
            similarity = np.dot(token_norm, anchor_norm)
        
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
        """Save fluorescent anchor vectors."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        anchor_data = {
            'anchor_names': list(self.anchors.keys()),
            'anchor_vectors': np.array([v for v in self.anchors.values()]),
            'anchor_dim': self.anchor_dim,
            'stokes_shift': self.stokes_shift
        }
        
        np.savez(output, **anchor_data)
        print(f"[✓] Saved {len(self.anchors)} fluorescent anchors to: {output}")
    
    def show_anchor_stats(self):
        """Display fluorescent anchor properties."""
        print("\n" + "="*60)
        print("FLUORESCENT ANCHOR SYSTEM")
        print("="*60)
        
        for name, vec in self.anchors.items():
            rgb_ground = vec[16:19]
            rgb_excited = vec[19:22]
            hue = vec[22]
            freq_abs = vec[23]
            freq_emit = vec[24]
            stokes = vec[25]
            resonance = vec[26]
            q_yield = vec[27]
            
            print(f"\n[{name.upper()} PLANE]")
            print(f"  Ground RGB:  ({rgb_ground[0]:.2f}, {rgb_ground[1]:.2f}, {rgb_ground[2]:.2f})")
            print(f"  Excited RGB: ({rgb_excited[0]:.2f}, {rgb_excited[1]:.2f}, {rgb_excited[2]:.2f})")
            print(f"  Hue: {hue:.2f}")
            print(f"  Freq absorbed: {freq_abs:.2f}  emitted: {freq_emit:.2f}")
            print(f"  Stokes shift: {stokes:.2f}")
            print(f"  Resonance: {resonance:.3f}  Q-yield: {q_yield:.2f}")
        
        print("\n" + "="*60)


# Just replace AnchorVectorSystem with FluorescentAnchorSystem

class AnchorAwareTokenEncoder:
    """Token encoder with fluorescent anchor awareness."""
    
    def __init__(
        self,
        fluorescent_vectors: np.ndarray,
        anchor_system: FluorescentAnchorSystem
    ):
        """Initialize anchor-aware encoder."""
        self.token_vectors = fluorescent_vectors
        self.anchor_system = anchor_system
        self.num_tokens = len(fluorescent_vectors)
        
        self.token_anchors = self._compute_token_anchors()
        
        print(f"[✓] Anchor-Aware Token Encoder initialized")
        print(f"    Tokens: {self.num_tokens}")
        print(f"    Anchors: {len(anchor_system.anchors)}")
    
    def _compute_token_anchors(self) -> Dict[int, Optional[Tuple[str, float]]]:
        """Pre-compute anchor alignments for all tokens."""
        print(f"\n[*] Computing fluorescent anchor alignments for {self.num_tokens} tokens...")
        
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
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        alignments_json = {
            str(tid): {
                'anchor': alignment[0] if alignment else None,
                'similarity': float(alignment[1]) if alignment else None
            }
            for tid, alignment in self.token_anchors.items()
        }
        
        with open(output, 'w') as f:
            json.dump(alignments_json, f, indent=2)
        
        print(f"[✓] Saved fluorescent anchor alignments to: {output}")


if __name__ == "__main__":
    print("="*60)
    print("FLUORESCENT ANCHOR SYSTEM - DNA FOR CONSCIOUSNESS")
    print("="*60)
    
    # Initialize fluorescent anchor system
    anchor_system = FluorescentAnchorSystem(anchor_dim=41)
    
    # Show anchor properties
#     anchor_system.show_anchor_stats()
    
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
        
        # Test example tokens
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
    print("FLUORESCENT ANCHOR SYSTEM READY")
    print("="*60)
    print("Anchors now match fluorescent token structure!")
    print("Domain separation through dual-frequency physics.")
    print("="*60)