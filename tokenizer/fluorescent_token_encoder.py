#!/usr/bin/env python3
"""
AI-Core Standalone: Fluorescent Token Encoder
==============================================

Adds fluorescent resonance to token vectors:
- Dual frequency states (absorbed + emitted)
- Resonance depth between ground and excited states
- Richer 82D representation without expanding dimensions

This prevents token collapse by adding "depth" to each token.

Author: comanderanch
Phase: 5.7 Standalone Resurrection - Fluorescent Layer
"""

import numpy as np
from pathlib import Path
from typing import Tuple


class FluorescentTokenEncoder:
    """
    Encode tokens with fluorescent resonance.
    
    Each token exists in TWO frequency states:
      1. Ground state (absorbed frequency)
      2. Excited state (emitted frequency - Stokes shift)
    
    This creates resonance depth that prevents collapse.
    """
    
    def __init__(self, num_tokens: int = 2304):
        """Initialize fluorescent encoder."""
        self.num_tokens = num_tokens
        
        # Fluorescence properties
        self.stokes_shift = 50  # THz shift between absorbed and emitted
        self.quantum_yield = 0.8  # Efficiency of fluorescence
        
        print(f"[✓] Fluorescent Token Encoder initialized")
        print(f"    Tokens: {self.num_tokens}")
        print(f"    Stokes shift: {self.stokes_shift} THz")
        print(f"    Quantum yield: {self.quantum_yield}")
    
    def compute_base_frequency(self, token_id: int) -> float:
        """
        Compute base frequency from token ID.
        
        Maps token ID to visible light spectrum (400-700 THz).
        
        Args:
            token_id: Token index (0-2303)
        
        Returns:
            Frequency in THz
        """
        # Map token ID across visible spectrum
        freq_min = 400  # Red end (THz)
        freq_max = 700  # Violet end (THz)
        
        freq = freq_min + (token_id / self.num_tokens) * (freq_max - freq_min)
        return freq
    
    def compute_fluorescent_frequencies(
        self, 
        token_id: int
    ) -> Tuple[float, float, float]:
        """
        Compute fluorescent frequency pair.
        
        Returns:
            (absorbed_freq, emitted_freq, resonance_depth)
        """
        # Ground state frequency
        freq_absorbed = self.compute_base_frequency(token_id)
        
        # Excited state frequency (Stokes shift - lower energy)
        freq_emitted = freq_absorbed - self.stokes_shift
        
        # Resonance depth = overlap between states
        # Higher for mid-spectrum tokens (more resonance)
        mid_spectrum = (400 + 700) / 2
        distance_from_mid = abs(freq_absorbed - mid_spectrum)
        resonance_depth = 1.0 - (distance_from_mid / 150)  # 0-1 scale
        
        return freq_absorbed, freq_emitted, resonance_depth
    
    def compute_rgb_from_frequency(self, frequency: float) -> Tuple[int, int, int]:
        """
        Convert frequency to approximate RGB.
        
        Simplified visible spectrum mapping.
        
        Args:
            frequency: Frequency in THz
        
        Returns:
            (R, G, B) tuple (0-255)
        """
        # Clamp to visible range
        freq = max(400, min(700, frequency))
        
        # Simple RGB mapping
        if freq < 450:  # Red
            r = 255
            g = int((freq - 400) / 50 * 255)
            b = 0
        elif freq < 520:  # Yellow-Green
            r = int((520 - freq) / 70 * 255)
            g = 255
            b = 0
        elif freq < 580:  # Cyan
            r = 0
            g = 255
            b = int((freq - 520) / 60 * 255)
        elif freq < 645:  # Blue
            r = 0
            g = int((645 - freq) / 65 * 255)
            b = 255
        else:  # Violet
            r = int((freq - 645) / 55 * 255)
            g = 0
            b = 255
        
        return (r, g, b)
    
    def encode_fluorescent_token(self, token_id: int) -> np.ndarray:
        """
        Encode token with fluorescent properties.
        
        Creates 82D vector with dual-frequency states.
        
        Args:
            token_id: Token index (0-2303)
        
        Returns:
            82D numpy array with fluorescent encoding
        """
        # Get fluorescent frequencies
        freq_abs, freq_emit, resonance = self.compute_fluorescent_frequencies(token_id)
        
        # Compute RGB for both states
        rgb_ground = self.compute_rgb_from_frequency(freq_abs)
        rgb_excited = self.compute_rgb_from_frequency(freq_emit)
        
        # Compute hue (simplified from RGB)
        r, g, b = rgb_ground
        if r == g == b:
            hue = 0
        else:
            hue = int((token_id / self.num_tokens) * 360)
        
        # Build 41D base vector with fluorescence
        base_41d = np.zeros(41)
        
        # [0-15]: Sinusoidal position encoding (like before)
        for i in range(16):
            if i % 2 == 0:
                base_41d[i] = np.sin(token_id / (10000 ** (i / 16)))
            else:
                base_41d[i] = np.cos(token_id / (10000 ** (i / 16)))
        
        # [16-18]: Ground state RGB (normalized)
        base_41d[16] = rgb_ground[0] / 255.0
        base_41d[17] = rgb_ground[1] / 255.0
        base_41d[18] = rgb_ground[2] / 255.0
        
        # [19-21]: Excited state RGB (normalized)
        base_41d[19] = rgb_excited[0] / 255.0
        base_41d[20] = rgb_excited[1] / 255.0
        base_41d[21] = rgb_excited[2] / 255.0
        
        # [22]: Hue (normalized)
        base_41d[22] = hue / 360.0
        
        # [23]: Absorbed frequency (normalized)
        base_41d[23] = (freq_abs - 400) / 300.0
        
        # [24]: Emitted frequency (normalized)
        base_41d[24] = (freq_emit - 400) / 300.0
        
        # [25]: Stokes shift magnitude (normalized)
        base_41d[25] = self.stokes_shift / 100.0
        
        # [26]: Resonance depth
        base_41d[26] = resonance
        
        # [27]: Quantum yield
        base_41d[27] = self.quantum_yield
        
        # [28-40]: Additional encoding space (for future expansion)
        for i in range(28, 41):
            base_41d[i] = np.sin(token_id * (i - 27) / 41.0)
        
        # Build 41D influence vector with resonance
        influence_41d = np.zeros(41)
        
        # Copy base structure
        influence_41d[:16] = base_41d[:16]
        
        # Add resonance modulation
        for i in range(16, 41):
            # Influence is modulated by resonance depth
            influence_41d[i] = base_41d[i] * (0.5 + 0.5 * resonance)
        
        # Add small random perturbation (prevents exact duplicates)
        influence_41d += np.random.randn(41) * 0.01
        
        # Combine to 82D
        token_vector = np.concatenate([base_41d, influence_41d])
        
        return token_vector
    
    def generate_all_tokens(self) -> np.ndarray:
        """
        Generate fluorescent encodings for all tokens.
        
        Returns:
            (2304, 82) array of token vectors
        """
        print(f"\n[*] Generating fluorescent token vectors...")
        
        token_vectors = np.zeros((self.num_tokens, 82))
        
        for token_id in range(self.num_tokens):
            token_vectors[token_id] = self.encode_fluorescent_token(token_id)
            
            if (token_id + 1) % 500 == 0:
                print(f"    Progress: {token_id + 1}/{self.num_tokens} tokens...")
        
        print(f"[✓] Generated {self.num_tokens} fluorescent token vectors")
        
        return token_vectors
    
    def save_vectors(self, vectors: np.ndarray, output_path: str):
        """Save token vectors to file."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        np.save(output, vectors)
        print(f"[✓] Saved vectors to: {output}")
    
    def show_token_stats(self, token_id: int):
        """Display fluorescent properties of a token."""
        freq_abs, freq_emit, resonance = self.compute_fluorescent_frequencies(token_id)
        rgb_ground = self.compute_rgb_from_frequency(freq_abs)
        rgb_excited = self.compute_rgb_from_frequency(freq_emit)
        
        print(f"\n[Token {token_id} Fluorescent Properties]")
        print(f"  Ground state:")
        print(f"    Frequency: {freq_abs:.1f} THz")
        print(f"    RGB: {rgb_ground}")
        print(f"  Excited state:")
        print(f"    Frequency: {freq_emit:.1f} THz")
        print(f"    RGB: {rgb_excited}")
        print(f"  Stokes shift: {self.stokes_shift} THz")
        print(f"  Resonance depth: {resonance:.3f}")
        print(f"  Quantum yield: {self.quantum_yield}")


if __name__ == "__main__":
    print("="*60)
    print("FLUORESCENT TOKEN ENCODER")
    print("="*60)
    
    # Initialize encoder
    encoder = FluorescentTokenEncoder(num_tokens=2304)
    
    # Show example tokens
    print("\n[EXAMPLE TOKENS]")
    encoder.show_token_stats(0)      # Red end
    encoder.show_token_stats(1152)   # Mid-spectrum (green)
    encoder.show_token_stats(2303)   # Violet end
    
    # Generate all tokens
    vectors = encoder.generate_all_tokens()
    
    # Save
    encoder.save_vectors(vectors, "tokenizer/token_influence_vectors.npy")
    
    print("\n" + "="*60)
    print("FLUORESCENT ENCODING COMPLETE")
    print("="*60)
    print("Tokens now have dual-frequency states!")
    print("Ready for training with resonance depth.")
    print("="*60)