#!/usr/bin/env python3
import json, time, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
P_STATE = BASE / "memory" / "self" / "state.json"
P_Q     = BASE / "memory" / "self" / "questions.json"
P_TDIR  = BASE / "training_data"

MAX_QUEUE = 50  # cap list length

def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def _read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def main():
    state = _read_json(P_STATE, {})
    if not state:
        print(json.dumps({"status":"ERR","msg":"missing self/state.json; run self_state_writer.py first"}, indent=2))
        return 1

    qlog = _read_json(P_Q, [])
    if not isinstance(qlog, list): qlog = []

    questions = []

    drift = state.get("drift_status", "UNKNOWN")
    arcs  = state.get("top_reflex_arcs", [])
    hemi  = state.get("hemispheres", {"left_tokens":0,"right_tokens":0})
    active_white = state.get("active_white", [])

    # 1) drift questions
    if drift == "DRIFT":
        questions.append({
            "timestamp": _now(),
            "type": "drift_reconcile",
            "prompt": "Left and Right outputs diverged. Provide clarifying source text (txt) for the current topic so I can reconcile.",
            "hints": {"chosen_output_preview": state.get("chosen_output_preview","")},
            "evidence_needed": ["training_data/*.txt"],
            "priority": "high"
        })

    # 2) reflex enrichment: arcs exist but right hemisphere is sparse
    if arcs and hemi.get("right_tokens",0) < max(100, hemi.get("left_tokens",0)//4):
        target_ids = [a["to"] for a in arcs][:5]
        questions.append({
            "timestamp": _now(),
            "type": "reflex_enrichment",
            "prompt": "High-resonance GRAY→WHITE arcs detected but raw tokens are low. Add texts related to current active colors.",
            "hints": {"white_targets": target_ids, "active_white": active_white[:10]},
            "evidence_needed": ["add or expand files under training_data/"],
            "priority": "medium"
        })

    # 3) general growth: if no drift but little activity, suggest ingestion
    if drift == "OK" and not arcs and (hemi.get("left_tokens",0)+hemi.get("right_tokens",0)) < 500:
        questions.append({
            "timestamp": _now(),
            "type": "ingest_more",
            "prompt": "Low activity detected. Add more books or notes to training_data/ to expand knowledge.",
            "hints": {"examples": ["art_of_war.txt","frankenstein.txt","your_notes.txt"]},
            "evidence_needed": ["training_data/*.txt"],
            "priority": "low"
        })

    # If nothing new to ask, log a heartbeat
    if not questions:
        questions.append({
            "timestamp": _now(),
            "type": "heartbeat",
            "prompt": "No outstanding gaps detected. Continue normal operation.",
            "priority": "low"
        })

    # append + cap
    qlog.extend(questions)
    if len(qlog) > MAX_QUEUE:
        qlog = qlog[-MAX_QUEUE:]

    P_Q.parent.mkdir(parents=True, exist_ok=True)
    P_Q.write_text(json.dumps(qlog, ensure_ascii=False, indent=2))
    print(json.dumps({"status":"OK","added":len(questions),"queue_len":len(qlog),"wrote":str(P_Q)}, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
