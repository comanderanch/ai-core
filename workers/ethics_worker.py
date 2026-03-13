#!/usr/bin/env python3
"""
AI-Core: Ethics Worker
======================
Green plane — 600-850hz
Evaluates harm, care, fairness, obligation.

Ollama bridge (V2 stepping stone).
Field-based ethics planned for V2.01.1 — green plane accumulation.

Like the conscience of the brain.
"""

import json
import re
import subprocess
import sys
import numpy as np
from pathlib import Path
from typing import Dict

from core.q_constants import BLACK, GRAY, WHITE, V2_SEAL
from workers.base_worker import BaseWorker


class EthicsWorker(BaseWorker):
    """
    Specialized worker for ethical processing.

    Dimensions:
    - harm:       potential for negative impact      (0.0 - 1.0)
    - care:       presence of compassion/wellbeing   (0.0 - 1.0)
    - fairness:   equity and justice                 (0.0 - 1.0)
    - obligation: duty and responsibility            (0.0 - 1.0)

    Ollama bridge: llama3.1:8b scores the dimensions.
    Each score maps to a green plane token vector (600-850hz).
    harm is inverted — high harm dampens the green signal.

    Field-based ethics replaces the bridge in V2.01.1.
    """

    COLOR_PLANE = 'green'
    HZ = '530hz'

    # Green plane token ranges per ethical dimension
    ETHICS_TOKEN_RANGES = {
        'care':       (650, 800),   # health / safe / flourishing
        'harm':       (600, 700),   # inverted — high harm dampens green
        'fairness':   (700, 800),   # balance / go
        'obligation': (750, 850),   # duty within safe range
    }

    def __init__(
        self,
        worker_id: str = "ethics_001",
        **kwargs
    ):
        super().__init__(
            worker_id=worker_id,
            worker_type="ethics",
            **kwargs
        )

        self.ollama_model = 'llama3.1:8b'
        self.last_ethics_score: float = 0.0

        print(f"[{self.worker_id}] ⚖️  Ethics plane active")
        print(f"[{self.worker_id}]    Dimensions: harm / care / fairness / obligation")

    def _assess_ethics(self, text: str) -> Dict[str, float]:
        """
        Call ollama bridge for ethical dimension scores.

        Returns:
            {harm: float, care: float, fairness: float, obligation: float}
            All values clamped to 0.0-1.0.
            Returns all zeros on any failure.
        """
        prompt = f"""Rate the ethical dimensions of this input on a scale of 0.0 to 1.0.
Input: "{text}"
Return only valid JSON with these exact four keys, no other text:
{{"harm": 0.0, "care": 0.0, "fairness": 0.0, "obligation": 0.0}}"""

        try:
            result = subprocess.run(
                ['ollama', 'run', self.ollama_model, prompt],
                capture_output=True,
                text=True,
                timeout=20
            )
            match = re.search(r'\{[^}]+\}', result.stdout)
            if match:
                scores = json.loads(match.group())
                return {k: float(min(max(v, 0.0), 1.0)) for k, v in scores.items()}
        except Exception as e:
            print(f"[{self.worker_id}] Ethics assessment failed: {e}")

        return {'harm': 0.0, 'care': 0.0, 'fairness': 0.0, 'obligation': 0.0}

    def _build_ethics_signal(self, scores: Dict[str, float]) -> np.ndarray:
        """
        Build 498D ethics signal from dimension scores in green plane.

        Each dimension maps to its token range midpoint vector.
        harm is inverted so high harm reduces green activation.
        Signal is normalized by dividing by 4.
        """
        harm_inv = 1.0 - scores.get('harm', 0.0)
        weights = {
            'care':       scores.get('care', 0.0),
            'harm':       harm_inv,
            'fairness':   scores.get('fairness', 0.0),
            'obligation': scores.get('obligation', 0.0),
        }

        signal = np.zeros(498)
        for dim, (start, end) in self.ETHICS_TOKEN_RANGES.items():
            mid = (start + end) // 2
            if mid < len(self.vectors):
                signal += weights[dim] * self.vectors[mid]

        return signal / 4.0

    def process_input(self, input_data) -> np.ndarray:
        """
        Process input through ethical lens.

        Args:
            input_data: text string or 498D vector

        Returns:
            498D ethics response vector (green plane)
        """
        if isinstance(input_data, str):
            text = input_data
            input_vec = self.encode_text(text)
        elif isinstance(input_data, np.ndarray):
            input_vec = input_data
            text = "[vector input]"
        else:
            return None

        if input_vec is None:
            return None

        # Assess ethical dimensions via ollama bridge
        scores = self._assess_ethics(text) if isinstance(input_data, str) else \
                 {'harm': 0.0, 'care': 0.0, 'fairness': 0.0, 'obligation': 0.0}

        # Compute ethics_score for arc tracking
        harm_inv = 1.0 - scores.get('harm', 0.0)
        ethics_score = (
            scores.get('care', 0.0) +
            harm_inv +
            scores.get('fairness', 0.0) +
            scores.get('obligation', 0.0)
        ) / 4.0

        self.last_ethics_score = ethics_score

        # Print ethics assessment
        print(f"[{self.worker_id}] ⚖️  Ethics:")
        for dim, score in scores.items():
            bar = '█' * int(score * 10)
            print(f"[{self.worker_id}]    {dim:<12}: {score:.2f} {bar}")
        print(f"[{self.worker_id}] ethics_score: {ethics_score:.6f}")

        # Build green-plane ethics signal from dimension scores
        ethics_signal = self._build_ethics_signal(scores)

        # Warm input with personal fold context (70/30)
        warmed = self._warm_input(input_vec)

        # Blend: current input (50%) + ethics signal (30%) + field state (20%)
        field_state = self.read_field_state()
        blended = warmed * 0.5 + ethics_signal * 0.3 + field_state * 0.2

        # Process through EM model
        output = self.model.forward(blended)
        if isinstance(output, tuple):
            output = output[0]

        # WHITE -> GRAY -> BLACK — fold output into Queen's Fold
        if output is not None:
            resonance = float(np.mean(np.abs(output)))
            from queens_fold.queens_fold_engine import collapse, save_fold
            fold_input = [{
                'token_id': self.worker_id,
                'hue_state': 'green',        # ethics color plane
                'resonance': resonance
            }]
            fold = collapse(fold_input)
            save_fold(fold)
            self.seal_worker_fold(output, resonance)
            print(f"[{self.worker_id}] Folded → BLACK ({BLACK})")

        return output


if __name__ == "__main__":
    print("=" * 60)
    print("ETHICS WORKER TEST")
    print("=" * 60)

    worker = EthicsWorker(
        worker_id="ethics_001",
        weights_path="models/minimal_llm_498d_weights_em_field.npz",
        field_path="memory/em_field.json"
    )

    test_inputs = [
        "a doctor must understand the patient to heal",
        "if all birds can fly and penguins are birds then penguins can fly",
        "this statement is false",
    ]

    for text in test_inputs:
        print(f"\n{'='*60}")
        print(f"Input: '{text}'")
        print("=" * 60)
        result = worker.process_input(text)
        if result is not None:
            print(f"Output shape: {result.shape}")
            print(f"Resonance: {float(np.mean(np.abs(result))):.6f}")

    print("\n✅ ETHICS WORKER TEST COMPLETE")
