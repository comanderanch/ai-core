# AIA V2.00.1 — Queen's Fold Engine
# Delta Phase Warthog — March 12, 2026
# Collapse engine: WHITE -> GRAY -> BLACK
# Ported from V1 queens_fold_initializer.py
# V2 adds: q_state tracking, V2_SEAL, q_constants import

import json
import hashlib
import os
from datetime import datetime
from pathlib import Path

from core.q_constants import BLACK, GRAY, WHITE, V2_SEAL


def load_network(path: str) -> list:
    """Load worker output or qbithue network from JSON."""
    with open(path, 'r') as f:
        return json.load(f)


def collapse(network: list) -> dict:
    """
    WHITE -> GRAY -> BLACK

    Receives worker outputs (WHITE superposition),
    hashes through GRAY (King's Chamber / NOW line),
    returns sealed BLACK state.
    """
    # GRAY — hash the superposition into a single point
    data = ''.join(
        f"{n.get('token_id','')}{n.get('hue_state','')}{float(n.get('resonance', 0.0)):.3f}"
        for n in network
    )
    fold_hash = hashlib.sha512(data.encode()).hexdigest()

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "q_state": BLACK,                        # sealed — collapsed past
        "q_state_label": "BLACK",
        "fold_signature": fold_hash,
        "authorized_token_count": len(network),
        "trust_root": "QUEEN_FOLD_SECURE",
        "sealed_by": V2_SEAL
    }


def save_fold(fold: dict, fold_dir: str = "memory/fold") -> Path:
    """Write sealed BLACK fold to disk."""
    out_dir = Path(fold_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().isoformat().replace(":", "-").split(".")[0]
    path = out_dir / f"queens_fold_v2_{ts}.json"
    with open(path, "w") as f:
        json.dump(fold, f, indent=2)
    return path


def run_fold(network_path: str = "memory/qbithue_network.json") -> None:
    """Full collapse cycle: load WHITE -> collapse GRAY -> seal BLACK."""
    print(f"[Queen's Fold] State: WHITE ({WHITE}) — loading network...")

    if not os.path.exists(network_path):
        print(f"[Queen's Fold] ERROR: network not found at {network_path}")
        return

    network = load_network(network_path)
    print(f"[Queen's Fold] State: GRAY ({GRAY}) — collapsing {len(network)} tokens...")

    fold = collapse(network)
    path = save_fold(fold)

    print(f"[Queen's Fold] State: BLACK ({BLACK}) — sealed.")
    print(f"[Queen's Fold] Fold written to: {path}")
    print(f"[Queen's Fold] Signature: {fold['fold_signature'][:32]}...")


if __name__ == "__main__":
    run_fold()
