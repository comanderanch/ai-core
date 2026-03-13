#!/usr/bin/env python3
"""
AI-Core: Consensus Worker
=========================
Gray plane — post-firing — runs after all workers complete.

Reads memory_001 × logic_001 output vectors.
Computes agreement, bridge, and gap.
Injects consensus signal into Queen's Fold before collapse.

Not a BaseWorker subclass — no ML stack, no word embeddings,
no EM field substrate. It processes the relationship between
two workers' outputs, not language.

Like the anterior cingulate cortex — conflict detection,
decision arbitration, consensus between stored knowledge
and active reasoning.
"""

import json
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from core.q_constants import BLACK, V2_SEAL


class ConsensusWorker:
    """
    Post-firing consensus: reads memory_001 × logic_001,
    computes agreement and bridge signal, injects into fold.

    Runs sequentially after threads.join() — cannot fire in
    parallel because it depends on other workers' output.

    Metrics:
    - agreement:     how aligned memory and logic are (0.0-1.0)
    - gap_magnitude: scalar divergence between the two planes
    - bridge_vec:    498D shared signal (average of both)
    - resonance:     mean(abs(bridge_vec)) — comparable to other workers
    """

    COLOR_PLANE = 'gray'
    HZ = '—'

    def __init__(self, fold_dir: str = "memory/worker_folds/consensus"):
        self.worker_id = 'consensus_001'
        self.worker_type = 'consensus'
        self.fold_dir = Path(fold_dir)
        self.fold_dir.mkdir(parents=True, exist_ok=True)
        self.personal_context: Optional[np.ndarray] = None  # prior bridge_vector

        self._load_worker_fold()
        print(f"[{self.worker_id}] ⚡ Consensus active — reads memory × logic")

    def _load_worker_fold(self):
        """Load most recent personal fold to warm bridge context."""
        folds = sorted(self.fold_dir.glob("fold_*.json"))
        if not folds:
            print(f"[{self.worker_id}] No personal fold — cold start")
            return
        latest = folds[-1]
        try:
            with open(latest) as f:
                data = json.load(f)
            self.personal_context = np.array(data['bridge_vector'])
            resonance = data.get('resonance', 0.0)
            agreement = data.get('agreement', 0.0)
            print(f"[{self.worker_id}] Personal fold loaded — "
                  f"resonance: {resonance:.6f}  agreement: {agreement:.4f}")
        except Exception as e:
            print(f"[{self.worker_id}] Personal fold load failed: {e}")

    def compute(self, results: Dict[str, np.ndarray]) -> Optional[dict]:
        """
        Compute consensus signal from memory_001 and logic_001 outputs.

        Args:
            results: {worker_id: output_vector} — populated after threads.join()

        Returns:
            {
                token_id, hue_state, resonance,
                agreement, gap_magnitude, bridge_vector
            }
            or None if either worker output is missing.
        """
        mem_vec = results.get('memory_001')
        log_vec = results.get('logic_001')

        if mem_vec is None or log_vec is None:
            print(f"[{self.worker_id}] Missing worker output — cannot compute")
            return None

        # Cosine similarity: agreement between memory and logic planes
        dot_product = float(np.dot(mem_vec, log_vec))
        norm_m = float(np.linalg.norm(mem_vec))
        norm_l = float(np.linalg.norm(log_vec))

        if norm_m > 1e-8 and norm_l > 1e-8:
            cosine_sim = dot_product / (norm_m * norm_l)
        else:
            cosine_sim = 0.0

        # Normalize cosine to 0.0-1.0
        agreement = float((cosine_sim + 1.0) / 2.0)

        # Bridge vector: shared signal between memory and logic
        bridge_vec = (mem_vec * 0.5 + log_vec * 0.5)

        # Gap vector: where memory and logic diverge
        gap_vec = mem_vec - log_vec
        gap_magnitude = float(np.linalg.norm(gap_vec))

        # Resonance: mean absolute value of bridge — same formula as all workers
        resonance = float(np.mean(np.abs(bridge_vec)))

        print(f"[{self.worker_id}]  memory × logic agreement : {agreement:.4f}")
        print(f"[{self.worker_id}]  gap magnitude            : {gap_magnitude:.4f}")
        print(f"[{self.worker_id}]  consensus_resonance      : {resonance:.6f}")

        return {
            'token_id':      'consensus_001',
            'hue_state':     'gray',
            'resonance':     resonance,
            'agreement':     agreement,
            'gap_magnitude': gap_magnitude,
            'bridge_vector': bridge_vec,
        }

    def seal_worker_fold(self, consensus_result: dict):
        """Seal consensus output as personal BLACK fold."""
        ts = datetime.utcnow().isoformat().replace(":", "-").split(".")[0]
        fold = {
            "worker_id":     self.worker_id,
            "worker_type":   self.worker_type,
            "color_plane":   self.COLOR_PLANE,
            "hz":            self.HZ,
            "resonance":     consensus_result['resonance'],
            "agreement":     consensus_result['agreement'],
            "gap_magnitude": consensus_result['gap_magnitude'],
            "bridge_vector": consensus_result['bridge_vector'].tolist(),
            "timestamp":     ts,
            "q_state":       BLACK,
            "q_state_label": "BLACK",
            "sealed_by":     V2_SEAL
        }
        path = self.fold_dir / f"fold_{self.worker_id}_{ts}.json"
        with open(path, 'w') as f:
            json.dump(fold, f, indent=2)
        self.personal_context = consensus_result['bridge_vector']
        print(f"[{self.worker_id}] Personal fold sealed → {path.name}")


if __name__ == "__main__":
    print("=" * 60)
    print("CONSENSUS WORKER TEST")
    print("=" * 60)

    worker = ConsensusWorker()

    # Simulate two worker output vectors
    mem_vec = np.random.randn(498)
    log_vec = np.random.randn(498)

    fake_results = {
        'memory_001': mem_vec,
        'logic_001':  log_vec,
    }

    print("\n--- Computing consensus ---")
    result = worker.compute(fake_results)

    if result:
        print(f"\nagreement    : {result['agreement']:.4f}")
        print(f"gap_magnitude: {result['gap_magnitude']:.4f}")
        print(f"resonance    : {result['resonance']:.6f}")
        worker.seal_worker_fold(result)
        print("\n✅ CONSENSUS WORKER TEST COMPLETE")
