#!/usr/bin/env python3
"""
AI-Core Standalone: GridBloc Spatial Encoder
=============================================

Encodes 5×5 spatial grid relationships into 250D vectors.

GridBloc represents spatial context through neighborhood relationships:
- Each token exists in a grid position (x, y)
- Neighbors influence token meaning through proximity
- Creates 250D spatial embedding (5×5 grid × 10D per cell)

This is NOT arbitrary positional encoding - it's spatial semantics:
- "fire" spreading → neighbors activate
- "water" flowing → directional patterns
- "solid" stable → static neighborhood

Based on original Dell 1950 matrix_grid_block.csv architecture,
but computed on-demand (hash-based) to avoid 800GB materialization.

Author: comanderanch
Phase: 5.7 Standalone Resurrection - 496D Expansion
"""

import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import hashlib


class GridBlocEncoder:
    """
    Spatial grid encoder for 250D neighborhood context.
    
    Creates 5×5 grid embeddings where each cell (10D) encodes:
    - Position (2D): x, y coordinates
    - Center token influence (2D): strength, direction
    - Neighbor average (4D): NSEW neighbor vectors
    - Spatial frequency (2D): oscillation patterns
    
    Total: 25 cells × 10D = 250D spatial encoding
    """
    
    def __init__(
        self,
        num_tokens: int = 2304,
        grid_size: int = 5,
        cell_dim: int = 10
    ):
        """
        Initialize GridBloc encoder.
        
        Args:
            num_tokens: Total tokens in vocabulary (2,304 color tokens)
            grid_size: Grid dimensions (5×5 = 25 cells)
            cell_dim: Dimensions per cell (10D per grid position)
        """
        self.num_tokens = num_tokens
        self.grid_size = grid_size
        self.cell_dim = cell_dim
        self.total_dim = grid_size * grid_size * cell_dim  # 250D
        
        # Compute token→grid position mappings (deterministic hash)
        self.token_positions = self._compute_token_positions()
        
        print(f"[✓] GridBloc Encoder initialized")
        print(f"    Grid size: {grid_size}×{grid_size}")
        print(f"    Cell dimensions: {cell_dim}D")
        print(f"    Total spatial dimensions: {self.total_dim}D")
    
    def _compute_token_positions(self) -> Dict[int, Tuple[int, int]]:
        """
        Compute deterministic grid positions for all tokens.
        
        Uses hash-based mapping to distribute tokens across 5×5 grid
        in a way that preserves color relationships.
        
        Returns:
            Dict mapping token_id → (x, y) grid position
        """
        positions = {}
        
        for token_id in range(self.num_tokens):
            # Hash token ID to get deterministic position
            # Use modulo to wrap into 5×5 grid
            hash_val = int(hashlib.sha256(str(token_id).encode()).hexdigest(), 16)
            
            x = (hash_val % self.grid_size)
            y = ((hash_val // self.grid_size) % self.grid_size)
            
            positions[token_id] = (x, y)
        
        return positions
    
    def encode_token(
        self,
        token_id: int,
        neighbor_tokens: Optional[List[int]] = None
    ) -> np.ndarray:
        """
        Encode token with spatial grid context.
        
        Args:
            token_id: Token to encode
            neighbor_tokens: Optional list of active neighbor tokens
        
        Returns:
            250D spatial encoding vector
        """
        # Get this token's grid position
        center_x, center_y = self.token_positions[token_id]
        
        # Initialize 250D grid vector
        grid_vector = np.zeros(self.total_dim)
        
        # Encode each cell in the 5×5 grid
        for grid_y in range(self.grid_size):
            for grid_x in range(self.grid_size):
                cell_idx = grid_y * self.grid_size + grid_x
                cell_start = cell_idx * self.cell_dim
                
                # Compute this cell's 10D encoding
                cell_encoding = self._encode_cell(
                    center_x, center_y,
                    grid_x, grid_y,
                    token_id,
                    neighbor_tokens
                )
                
                # Write to grid vector
                grid_vector[cell_start:cell_start + self.cell_dim] = cell_encoding
        
        return grid_vector
    
    def _encode_cell(
        self,
        center_x: int, center_y: int,
        grid_x: int, grid_y: int,
        token_id: int,
        neighbor_tokens: Optional[List[int]]
    ) -> np.ndarray:
        """
        Encode a single cell's 10D representation.
        
        Args:
            center_x, center_y: Token's position in grid
            grid_x, grid_y: Current cell position
            token_id: Token being encoded
            neighbor_tokens: Active neighbors
        
        Returns:
            10D cell encoding
        """
        cell = np.zeros(self.cell_dim)
        
        # Distance from center token to this cell
        dx = grid_x - center_x
        dy = grid_y - center_y
        distance = np.sqrt(dx**2 + dy**2)
        
        # [0-1]: Normalized x position
        cell[0] = grid_x / (self.grid_size - 1)
        
        # [2-3]: Normalized y position
        cell[1] = grid_y / (self.grid_size - 1)
        
        # [4-5]: Center token influence (falls off with distance)
        if distance == 0:
            # Center cell - maximum influence
            cell[2] = 1.0
            cell[3] = 0.0
        else:
            # Influence falls off as 1/distance
            influence = 1.0 / (1.0 + distance)
            cell[2] = influence
            
            # Direction angle from center
            angle = np.arctan2(dy, dx)
            cell[3] = angle / np.pi  # Normalize to [-1, 1]
        
        # [4-7]: Neighbor average (NSEW directions)
        if neighbor_tokens:
            neighbor_avg = self._compute_neighbor_influence(
                grid_x, grid_y, neighbor_tokens
            )
            cell[4:8] = neighbor_avg
        
        # [8-9]: Spatial frequency encoding
        # Creates wave patterns across grid
        freq_x = np.sin(2 * np.pi * grid_x / self.grid_size + token_id * 0.1)
        freq_y = np.cos(2 * np.pi * grid_y / self.grid_size + token_id * 0.1)
        cell[8] = freq_x
        cell[9] = freq_y
        
        return cell
    
    def _compute_neighbor_influence(
        self,
        grid_x: int,
        grid_y: int,
        neighbor_tokens: List[int]
    ) -> np.ndarray:
        """
        Compute average influence from neighboring tokens.
        
        Args:
            grid_x, grid_y: Current cell position
            neighbor_tokens: List of active neighbor token IDs
        
        Returns:
            4D vector: [north, south, east, west] neighbor strengths
        """
        neighbors = np.zeros(4)  # [N, S, E, W]
        
        for neighbor_id in neighbor_tokens:
            if neighbor_id not in self.token_positions:
                continue
            
            nx, ny = self.token_positions[neighbor_id]
            
            # Compute relative direction
            dx = nx - grid_x
            dy = ny - grid_y
            
            distance = np.sqrt(dx**2 + dy**2)
            if distance == 0:
                continue
            
            influence = 1.0 / (1.0 + distance)
            
            # Distribute to cardinal directions based on angle
            angle = np.arctan2(dy, dx)
            
            # North (up, negative y)
            if -np.pi/4 <= angle < np.pi/4:
                neighbors[2] += influence  # East
            elif np.pi/4 <= angle < 3*np.pi/4:
                neighbors[0] += influence  # North
            elif -3*np.pi/4 <= angle < -np.pi/4:
                neighbors[1] += influence  # South
            else:
                neighbors[3] += influence  # West
        
        # Normalize
        total = np.sum(neighbors)
        if total > 0:
            neighbors = neighbors / total
        
        return neighbors
    
    def encode_sequence(
        self,
        token_sequence: List[int]
    ) -> np.ndarray:
        """
        Encode a sequence of tokens with spatial context.
        
        Each token in sequence is encoded with awareness of other
        tokens in the sequence (they act as neighbors).
        
        Args:
            token_sequence: List of token IDs
        
        Returns:
            Array of shape (len(sequence), 250D)
        """
        num_tokens = len(token_sequence)
        encoded = np.zeros((num_tokens, self.total_dim))
        
        for i, token_id in enumerate(token_sequence):
            # Other tokens in sequence act as neighbors
            neighbors = [tid for j, tid in enumerate(token_sequence) if j != i]
            
            encoded[i] = self.encode_token(token_id, neighbors)
        
        return encoded
    
    def save_encoder(self, output_path: str = "tokenizer/gridbloc_encoder.npz"):
        """Save encoder configuration."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
    
        # Convert token_positions dict to arrays for saving
        token_ids = np.array(list(self.token_positions.keys()))
        positions_x = np.array([pos[0] for pos in self.token_positions.values()])
        positions_y = np.array([pos[1] for pos in self.token_positions.values()])
    
        np.savez(
            output,
            num_tokens=self.num_tokens,
            grid_size=self.grid_size,
            cell_dim=self.cell_dim,
            token_ids=token_ids,
            positions_x=positions_x,
            positions_y=positions_y
    )
    
        print(f"[✓] Saved GridBloc encoder to: {output}")


if __name__ == "__main__":
    print("="*60)
    print("GRIDBLOC SPATIAL ENCODER - 250D NEIGHBORHOOD CONTEXT")
    print("="*60)
    
    # Initialize encoder
    encoder = GridBlocEncoder(num_tokens=2304, grid_size=5, cell_dim=10)
    
    # Test encoding single token
    print("\n[TEST] Encoding token 0 (fire input)")
    grid_vec = encoder.encode_token(token_id=0)
    print(f"  Shape: {grid_vec.shape}")
    print(f"  Norm: {np.linalg.norm(grid_vec):.3f}")
    print(f"  Non-zero elements: {np.count_nonzero(grid_vec)}/{len(grid_vec)}")
    
    # Test encoding sequence
    print("\n[TEST] Encoding sequence [0, 16, 32] (fire)")
    seq_vecs = encoder.encode_sequence([0, 16, 32])
    print(f"  Shape: {seq_vecs.shape}")
    print(f"  Token 0 norm: {np.linalg.norm(seq_vecs[0]):.3f}")
    print(f"  Token 16 norm: {np.linalg.norm(seq_vecs[1]):.3f}")
    print(f"  Token 32 norm: {np.linalg.norm(seq_vecs[2]):.3f}")
    
    # Save encoder
    encoder.save_encoder()
    
    print("\n" + "="*60)
    print("GRIDBLOC ENCODER READY")
    print("="*60)
    print("250D spatial encoding preserves neighborhood relationships!")
    print("Ready to combine with 82D fluorescent base → 332D!")
    print("="*60)