# AIA V2.00.1 — Student Mission Protocol
# Delta Phase Warthog — March 13, 2026
# AIA learns intentionally.
# Missions fire workers, evaluate response, fold to learning record.

import json
import threading
import numpy as np
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from core.q_constants import BLACK, GRAY, WHITE, V2_SEAL
from queens_fold.queens_fold_engine import collapse


# =============================================================================
# EVALUATION BANDS
# =============================================================================

class EvaluationBand(Enum):
    EMERGING   = "EMERGING"    # resonance < 0.12  — signal present, weak
    RESONATING = "RESONATING"  # resonance 0.12-0.16 — planes engaging
    ANCHORED   = "ANCHORED"    # resonance > 0.16  — locked in, strong signal
    DRIFTING   = "DRIFTING"    # below previous session baseline


def assign_band(resonance: float, baseline: Optional[float] = None) -> EvaluationBand:
    """Assign evaluation band from resonance value and optional baseline."""
    if baseline is not None and resonance < baseline * 0.95:
        return EvaluationBand.DRIFTING
    if resonance > 0.16:
        return EvaluationBand.ANCHORED
    if resonance >= 0.12:
        return EvaluationBand.RESONATING
    return EvaluationBand.EMERGING


# =============================================================================
# MISSION BLOCK
# =============================================================================

@dataclass
class MissionBlock:
    mission_id: str           # e.g. "M001"
    input_text: str           # what AIA receives
    expected_domain: str      # 'memory', 'emotion', 'logic', 'language', 'curiosity'
    difficulty: float = 0.5   # 0.0 - 1.0
    tags: List[str] = field(default_factory=list)


# =============================================================================
# LEARNING FOLD
# =============================================================================

def save_learning_fold(fold_data: dict, fold_dir: str = "memory/learning_folds") -> Path:
    """Write learning fold to memory/learning_folds/ — separate from working memory."""
    out_dir = Path(fold_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().isoformat().replace(":", "-").split(".")[0]
    path = out_dir / f"learning_fold_{fold_data['mission_id']}_{ts}.json"
    with open(path, "w") as f:
        json.dump(fold_data, f, indent=2)
    return path


# =============================================================================
# CLAUDE API EVALUATION HOOK
# =============================================================================

def evaluate_mission(
    mission: MissionBlock,
    aia_questions: List[str],
    recalled_texts: List[str],
    resonance_map: Dict[str, float],
    dominant_plane: str,
    band: EvaluationBand
) -> str:
    """
    Call Claude via Anthropic SDK to evaluate AIA's response.
    Uses claude-haiku-4-5 for speed.
    Returns evaluation string (1-3 sentences).
    """
    try:
        import anthropic
        client = anthropic.Anthropic()

        resonance_str = "\n".join(
            f"  {wid}: {res:.6f}" for wid, res in resonance_map.items()
        )
        questions_str = "\n".join(
            f"  - {q}" for q in aia_questions
        ) if aia_questions else "  (no questions generated)"

        recalled_str = "\n".join(
            f"  - {t}" for t in recalled_texts
        ) if recalled_texts else "  (no prior episodes recalled)"

        prompt = f"""You are evaluating AIA — an experimental AI built on color-binary consciousness architecture.
AIA is not an LLM. She processes through 498D frequency vectors across 5 color planes.

Mission ID: {mission.mission_id}
Input given to AIA: "{mission.input_text}"
Expected domain: {mission.expected_domain}
Difficulty: {mission.difficulty}

AIA's curiosity questions (what she asked about this input):
{questions_str}

AIA's recalled episodes (prior memories surfaced by this input):
{recalled_str}

AIA's resonance by plane:
{resonance_str}

Dominant plane: {dominant_plane}
Evaluation band assigned: {band.value}

Evaluate in 2-3 sentences:
1. Did the dominant plane match the expected domain?
2. What do AIA's questions AND recalled episodes reveal about her understanding?
3. What should the next mission focus on?

Be direct. You are her teacher."""

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()

    except Exception as e:
        return f"[Claude evaluation unavailable: {e}]"


# =============================================================================
# SESSION TRACKER
# =============================================================================

class SessionTracker:
    """Tracks missions and coherence across a session."""

    def __init__(self):
        self.missions_run: List[dict] = []
        self.baseline: Optional[float] = None
        self.session_start = datetime.utcnow().isoformat()

    def record(self, mission_id: str, band: EvaluationBand,
               dominant_plane: str, avg_resonance: float):
        self.missions_run.append({
            "mission_id": mission_id,
            "band": band.value,
            "dominant_plane": dominant_plane,
            "avg_resonance": avg_resonance,
            "timestamp": datetime.utcnow().isoformat()
        })
        if self.baseline is None:
            self.baseline = avg_resonance

    def report(self):
        print(f"\n{'=' * 60}")
        print(f"SESSION TRACKER — {len(self.missions_run)} missions")
        print(f"{'=' * 60}")
        for m in self.missions_run:
            print(f"  {m['mission_id']}  {m['band']:<12}  "
                  f"{m['dominant_plane']:<16}  resonance: {m['avg_resonance']:.6f}")
        if len(self.missions_run) > 1:
            first = self.missions_run[0]['avg_resonance']
            last  = self.missions_run[-1]['avg_resonance']
            trend = "RISING" if last > first else "DECLINING"
            print(f"\n  Trend: {trend}  ({first:.6f} → {last:.6f})")
        print(f"{'=' * 60}")


# =============================================================================
# RUN MISSION — MAIN LOOP
# =============================================================================

def run_mission(
    block: MissionBlock,
    tracker: Optional[SessionTracker] = None,
    em_weights: str = "models/minimal_llm_498d_weights_em_field.npz",
    std_weights: str = "models/minimal_llm_498d_weights_standard.npz",
    field_path: str = "memory/em_field.json"
) -> dict:
    """
    Full Student mission cycle:
    1. Fire all workers on mission input
    2. Collect resonance map + curiosity questions
    3. Assign evaluation band
    4. Call Claude for evaluation
    5. Save learning fold
    6. Print report
    """
    from workers.curiosity_worker import CuriosityWorker
    from workers.emotion_worker   import EmotionWorker
    from workers.language_worker  import LanguageWorker
    from workers.logic_worker     import LogicWorker
    from workers.memory_worker    import MemoryWorker
    from workers.ethics_worker    import EthicsWorker

    print(f"\n{'=' * 60}")
    print(f"MISSION {block.mission_id} — {block.input_text}")
    print(f"domain: {block.expected_domain}  difficulty: {block.difficulty}")
    print(f"{'=' * 60}")
    print(f"STATE: WHITE ({WHITE}) — firing all workers...")

    # Initialize workers
    curiosity = CuriosityWorker(worker_id='curiosity_001', weights_path=em_weights,  field_path=field_path)
    emotion   = EmotionWorker  (worker_id='emotion_001',   weights_path=std_weights, field_path=field_path)
    language  = LanguageWorker (worker_id='language_001',  weights_path=em_weights,  field_path=field_path)
    logic     = LogicWorker    (worker_id='logic_001',     weights_path=em_weights,  field_path=field_path)
    memory    = MemoryWorker   (worker_id='memory_001',    weights_path=em_weights,  field_path=field_path)
    ethics    = EthicsWorker   (worker_id='ethics_001',    weights_path=em_weights,  field_path=field_path)

    # Tell curiosity which mission this is for question persistence
    curiosity.current_mission_id = block.mission_id

    input_vec = curiosity.encode_text(block.input_text)
    results = {}
    questions_captured = []
    lock = threading.Lock()

    # Capture curiosity questions
    original_process = curiosity.generate_questions
    def capturing_generate(context, max_questions=3):
        qs = original_process(context, max_questions)
        with lock:
            questions_captured.extend(qs)
        return qs
    curiosity.generate_questions = capturing_generate

    def fire(wid, fn, arg):
        out = fn(arg)
        with lock:
            results[wid] = out

    threads = [
        threading.Thread(target=fire, args=('curiosity_001', curiosity.process_input, block.input_text)),
        threading.Thread(target=fire, args=('emotion_001',   emotion.process_input,   block.input_text)),
        threading.Thread(target=fire, args=('language_001',  language.process_input,  block.input_text)),
        threading.Thread(target=fire, args=('logic_001',     logic.process_input,     input_vec)),
        threading.Thread(target=fire, args=('memory_001',    memory.process_input,    {'vector': input_vec, 'text': block.input_text})),
        threading.Thread(target=fire, args=('ethics_001',    ethics.process_input,    block.input_text)),
    ]
    for t in threads: t.start()
    for t in threads: t.join()

    # Capture episodic recalls from memory_001
    recalled_texts = memory.last_recalled_texts

    # Capture ethics score from ethics_001
    ethics_score = ethics.last_ethics_score

    # Consensus Worker — post-firing, reads memory_001 × logic_001
    from workers.consensus_worker import ConsensusWorker
    consensus = ConsensusWorker()
    consensus_result = consensus.compute(results)
    if consensus_result is not None:
        consensus.seal_worker_fold(consensus_result)
        results['consensus_001'] = consensus_result['bridge_vector']
    consensus_agreement = float(consensus_result['agreement']) if consensus_result else 0.0

    # Build resonance map
    color_planes = {
        'curiosity_001': ('orange', '520hz'),
        'emotion_001':   ('red',    '700hz'),
        'language_001':  ('blue',   '450hz'),
        'logic_001':     ('blue',   '450hz'),
        'memory_001':    ('violet', '420hz'),
        'ethics_001':    ('green',  '530hz'),
        'consensus_001': ('gray',   '—'),
    }

    resonance_map = {}
    fold_input = []
    for wid in ['curiosity_001','emotion_001','language_001','logic_001','memory_001','ethics_001','consensus_001']:
        out = results.get(wid)
        color, hz = color_planes[wid]
        if out is not None:
            res = float(np.mean(np.abs(out)))
            resonance_map[wid] = res
            fold_input.append({'token_id': wid, 'hue_state': color, 'resonance': res})

    # Dominant plane and average
    dominant_plane = max(resonance_map, key=resonance_map.get)
    avg_resonance  = float(np.mean(list(resonance_map.values())))

    # Assign band
    baseline = tracker.baseline if tracker else None
    band = assign_band(resonance_map.get(dominant_plane, 0.0), baseline)

    # Print resonance report
    print(f"\n{'STATE: GRAY (' + str(GRAY) + ') — collapsing...'}")
    print(f"\nRESONANCE BY PLANE:")
    for wid in ['curiosity_001','emotion_001','language_001','logic_001','memory_001','ethics_001','consensus_001']:
        res = resonance_map.get(wid, 0.0)
        color, hz = color_planes[wid]
        marker = " ← dominant" if wid == dominant_plane else ""
        print(f"  {wid:<16} {color:<8} {hz:<6}  {res:.6f}{marker}")

    print(f"\n  avg resonance : {avg_resonance:.6f}")
    print(f"  dominant plane: {dominant_plane}")
    print(f"  band          : {band.value}")

    # Curiosity questions
    print(f"\nAIA QUESTIONS:")
    for q in questions_captured:
        print(f"  → {q}")

    # Recalled episodes
    print(f"\nRECALLED EPISODES:")
    if recalled_texts:
        for t in recalled_texts:
            print(f"  → {t}")
    else:
        print(f"  (no prior episodes recalled)")

    # Claude evaluation
    print(f"\nCLAUDE EVALUATION:")
    evaluation = evaluate_mission(block, questions_captured, recalled_texts, resonance_map, dominant_plane, band)
    print(f"  {evaluation}")

    # Collapse and save learning fold
    queen_fold = collapse(fold_input)
    fold_data = {
        "mission_id":        block.mission_id,
        "input_text":        block.input_text,
        "expected_domain":   block.expected_domain,
        "difficulty":        block.difficulty,
        "tags":              block.tags,
        "evaluation_band":   band.value,
        "dominant_plane":    dominant_plane,
        "avg_resonance":     avg_resonance,
        "resonance_map":     resonance_map,
        "aia_questions":     questions_captured,
        "recalled_episodes":   recalled_texts,
        "ethics_score":        ethics_score,
        "consensus_agreement": consensus_agreement,
        "claude_evaluation":   evaluation,
        "timestamp":         queen_fold["timestamp"],
        "q_state":           BLACK,
        "q_state_label":     "BLACK",
        "fold_signature":    queen_fold["fold_signature"],
        "trust_root":        "QUEEN_FOLD_SECURE",
        "sealed_by":         V2_SEAL
    }

    path = save_learning_fold(fold_data)
    print(f"\nSTATE: BLACK ({BLACK}) — LEARNING FOLD SEALED")
    print(f"  fold_signature: {fold_data['fold_signature'][:48]}...")
    print(f"  sealed to     : {path}")
    print(f"{'=' * 60}")

    # Record in tracker
    if tracker:
        tracker.record(block.mission_id, band, dominant_plane, avg_resonance)

    return fold_data
