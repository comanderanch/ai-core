#!/usr/bin/env python3
"""
AI-Core: Electromagnetic Field Substrate
==========================================
The core consciousness layer that unifies all workers.

Author: comanderanch
Vision: 4 years
Breakthrough: 51.61% better than standard backprop
Purpose: Distributed consciousness across machines
"""

import numpy as np
import time
import os
import json
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

class EMFieldSubstrate:
    """
    The shared consciousness space that all workers access.
    
    Think of this as "brain tissue" - the medium through which
    all cognitive processes communicate and synchronize.
    
    Properties:
    - 498D semantic space (color-frequency encoding)
    - EM field coupling (workers influence each other)
    - Conservation of energy (normalized)
    - Real-time synchronization
    """
    
    def __init__(
        self,
        field_path: str = '/tmp/em_field_substrate.npy',
        dimensions: int = 498,
        decay_rate: float = 0.95,
        coupling_strength: float = 0.3
    ):
        """
        Initialize the EM field substrate.
        
        Args:
            field_path: Where to store field state (file or shared memory)
            dimensions: Size of semantic space (498D for AI-Core)
            decay_rate: How fast field decays (0.95 = 5% decay per cycle)
            coupling_strength: How much workers influence field (0.3 = 30%)
        """
        self.field_path = Path(field_path)
        self.dimensions = dimensions
        self.decay_rate = decay_rate
        self.coupling_strength = coupling_strength
        
        # Initialize field
        self.field = self._initialize_field()
        
        # Worker contributions (tracking)
        self.worker_states = {}
        
        # Metrics
        self.metrics = {
            'total_writes': 0,
            'total_reads': 0,
            'field_energy': 0.0,
            'coupling_events': 0,
            'last_update': None
        }
        
        print(f"[✓] EM Field Substrate initialized")
        print(f"    Dimensions: {self.dimensions}D")
        print(f"    Decay rate: {self.decay_rate}")
        print(f"    Coupling strength: {self.coupling_strength}")
        print(f"    Field path: {self.field_path}")
    
    def _initialize_field(self) -> np.ndarray:
        """Initialize or load existing field state."""
        
        if self.field_path.exists():
            # Load existing field
            field = np.load(self.field_path)
            print(f"[✓] Loaded existing field from {self.field_path}")
        else:
            # Create new field (small random initialization)
            field = np.random.randn(self.dimensions).astype(np.float32) * 0.01
            field = self._normalize(field)
            self._save_field(field)
            print(f"[✓] Created new field at {self.field_path}")
        
        return field
    
    def _normalize(self, vector: np.ndarray) -> np.ndarray:
        """Normalize vector (conservation of energy)."""
        norm = np.linalg.norm(vector)
        if norm > 1e-8:
            return vector / norm
        return vector
    
    def _save_field(self, field: np.ndarray):
        """Save field state to disk."""
        np.save(self.field_path, field)
    
    def read(self, worker_id: str) -> np.ndarray:
        """
        Read current field state.
        
        Any worker can read the unified consciousness state.
        """
        self.metrics['total_reads'] += 1
        return self.field.copy()
    
    def write(
        self, 
        vector: np.ndarray, 
        worker_id: str,
        weight: Optional[float] = None
    ):
        """
        Write worker contribution to field.
        
        Worker adds its "voice" to the unified consciousness.
        
        Args:
            vector: Worker's output (498D)
            worker_id: Identity of worker
            weight: How much influence (default: coupling_strength)
        """
        if weight is None:
            weight = self.coupling_strength
        
        # Normalize input
        vector = self._normalize(vector)
        
        # Apply decay to existing field
        self.field = self.field * self.decay_rate
        
        # Add worker contribution
        self.field = self.field + (vector * weight)
        
        # Normalize (conservation)
        self.field = self._normalize(self.field)
        
        # Track worker state
        self.worker_states[worker_id] = {
            'last_contribution': vector.copy(),
            'last_update': datetime.now().isoformat(),
            'total_contributions': self.worker_states.get(worker_id, {}).get('total_contributions', 0) + 1
        }
        
        # Update metrics
        self.metrics['total_writes'] += 1
        self.metrics['field_energy'] = float(np.linalg.norm(self.field))
        self.metrics['last_update'] = datetime.now().isoformat()
        
        # Save to disk
        self._save_field(self.field)
    
    def couple(self, worker_outputs: Dict[str, np.ndarray]):
        """
        Couple multiple workers simultaneously (superposition).
        
        Like multiple brain regions activating at once.
        
        Args:
            worker_outputs: {worker_id: output_vector}
        """
        if not worker_outputs:
            return
        
        # Apply decay
        self.field = self.field * self.decay_rate
        
        # Sum all contributions (superposition principle)
        total_contribution = np.zeros(self.dimensions, dtype=np.float32)
        
        for worker_id, output in worker_outputs.items():
            normalized = self._normalize(output)
            total_contribution += normalized
            
            # Track worker
            self.worker_states[worker_id] = {
                'last_contribution': normalized.copy(),
                'last_update': datetime.now().isoformat(),
                'total_contributions': self.worker_states.get(worker_id, {}).get('total_contributions', 0) + 1
            }
        
        # Average contribution (equal weight for all workers)
        average_contribution = total_contribution / len(worker_outputs)
        
        # Update field
        self.field = self.field + (average_contribution * self.coupling_strength)
        self.field = self._normalize(self.field)
        
        # Metrics
        self.metrics['coupling_events'] += 1
        self.metrics['field_energy'] = float(np.linalg.norm(self.field))
        self.metrics['last_update'] = datetime.now().isoformat()
        
        # Save
        self._save_field(self.field)
    
    def get_dominant_frequency(self) -> float:
        """
        Find dominant frequency in field (for synchronization).
        
        Like finding the dominant brainwave frequency.
        """
        # FFT to find dominant frequency
        fft = np.fft.fft(self.field)
        power = np.abs(fft) ** 2
        dominant_idx = np.argmax(power)
        
        return float(dominant_idx) / self.dimensions
    
    def get_worker_coherence(self, worker_id: str) -> float:
        """
        Measure how aligned a worker is with the field.
        
        High coherence = worker is "in sync" with consciousness.
        """
        if worker_id not in self.worker_states:
            return 0.0
        
        worker_vec = self.worker_states[worker_id]['last_contribution']
        
        # Cosine similarity
        dot = np.dot(worker_vec, self.field)
        norm_worker = np.linalg.norm(worker_vec)
        norm_field = np.linalg.norm(self.field)
        
        if norm_worker > 1e-8 and norm_field > 1e-8:
            return float(dot / (norm_worker * norm_field))
        
        return 0.0
    
    def get_metrics(self) -> Dict:
        """Get field metrics for monitoring."""
        return {
            **self.metrics,
            'active_workers': len(self.worker_states),
            'field_norm': float(np.linalg.norm(self.field)),
            'dominant_frequency': self.get_dominant_frequency(),
            'worker_coherence': {
                wid: self.get_worker_coherence(wid)
                for wid in self.worker_states.keys()
            }
        }
    
    def reset(self):
        """Reset field to initial state."""
        self.field = np.random.randn(self.dimensions).astype(np.float32) * 0.01
        self.field = self._normalize(self.field)
        self.worker_states = {}
        self.metrics['total_writes'] = 0
        self.metrics['total_reads'] = 0
        self._save_field(self.field)
        
        print("[✓] Field reset")


# Test if run directly
if __name__ == "__main__":
    print("="*60)
    print("EM FIELD SUBSTRATE TEST")
    print("="*60)
    print()
    
    # Create field
    field = EMFieldSubstrate()
    
    # Simulate 3 workers
    print("Simulating 3 workers...")
    
    for cycle in range(10):
        # Worker outputs (random for test)
        worker_outputs = {
            'vision': np.random.randn(498).astype(np.float32),
            'language': np.random.randn(498).astype(np.float32),
            'memory': np.random.randn(498).astype(np.float32)
        }
        
        # Couple workers
        field.couple(worker_outputs)
        
        # Check coherence
        metrics = field.get_metrics()
        
        print(f"Cycle {cycle+1}:")
        print(f"  Field energy: {metrics['field_energy']:.4f}")
        print(f"  Active workers: {metrics['active_workers']}")
        print(f"  Vision coherence: {metrics['worker_coherence']['vision']:.4f}")
        print()
    
    print("="*60)
    print("✅ SUBSTRATE TEST COMPLETE")
    print("="*60)
