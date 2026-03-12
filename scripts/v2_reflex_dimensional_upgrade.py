#!/usr/bin/env python3
"""
AIA V2.00.1 — Dimensional Reflex Logging Upgrade
==================================================
Delta Phase Warthog — March 12, 2026

What this does:
  Upgrades the reflex log structure to include color_plane + frequency.
  This makes ALL corrections happen in dimensional space — not flat scalar.

Before (V1 reflex log entry):
  {"reflex": "curiosity_reflex", "timestamp": "..."}

After (V2 reflex log entry):
  {
    "reflex": "curiosity_reflex",
    "color_plane": [255, 140, 0],    # RGB — the frequency plane this fired in
    "frequency": 520.0,              # Hz — position in that plane
    "hue_shift": +3.2,               # how far from center of that color plane
    "q_state": 1,                    # WHITE=+1 (fired in superposition)
    "timestamp": "..."
  }

Why this matters:
  Without color_plane: correction engine applies flat scalar to ALL planes equally
  With color_plane:    correction engine corrects ONLY the plane that drifted
  
  Example:
    "curiosity_reflex" drifts in the ORANGE plane (freq 520hz)
    V1 corrects: ALL curiosity weight reduced by -drift × 0.5
    V2 corrects: ONLY orange plane curiosity weight reduced
    
    Blue plane curiosity (calm/analytical) stays untouched.
    That's the difference between a flat response and a dimensional one.

HOW TO DEPLOY:
  Step 1: Run this script — it upgrades existing log entries
  Step 2: Replace the 5 log functions in your scripts with the ones below
  Step 3: That's it. The rest of the pipeline reads the same structure.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# ── V2 Q-State constants ──────────────────────────────────────────────────────
BLACK = -1   # Collapsed past — sealed memory
GRAY  =  0   # Zero point — NOW line — King's Chamber
WHITE = +1   # Superposition — future possibilities

# ── Color plane registry ──────────────────────────────────────────────────────
# Each cognitive function has a home frequency plane.
# These are the base assignments — they can be extended.
# The hue_shift moves ± from the center of each plane.
#
# This is where the palette meets the cybernetic system.
# A reflex that fires in RED space carries different weight
# than the same reflex firing in BLUE space.

COLOR_PLANES = {
    # name          : (R,   G,   B,   center_freq_hz)
    "red"           : (255,   0,   0,  700.0),  # High activation / urgency
    "orange"        : (255, 140,   0,  520.0),  # Curiosity / exploration
    "yellow"        : (255, 255,   0,  580.0),  # Attention / focus
    "green"         : (  0, 255,   0,  540.0),  # Growth / learning / balance
    "cyan"          : (  0, 255, 255,  490.0),  # Clarity / processing
    "blue"          : (  0,   0, 255,  450.0),  # Calm / logic / deep recall
    "violet"        : (148,   0, 211,  420.0),  # Intuition / pattern recognition
    "white"         : (255, 255, 255,  760.0),  # Full superposition / open state
    "black"         : (  0,   0,   0,  380.0),  # Collapsed / sealed memory
    "gray"          : (128, 128, 128,  400.0),  # NOW line / fold anchor / zero point
}

# Reflex → color plane mapping
# When a reflex fires, this tells us which dimensional plane it belongs to.
# Add new reflexes here as they are discovered.
REFLEX_PLANE_MAP = {
    # Curiosity / exploration reflexes → orange plane
    "curiosity_reflex"          : "orange",
    "exploration_reflex"        : "orange",
    "question_reflex"           : "orange",

    # Logic / analysis reflexes → blue plane
    "logic_reflex"              : "blue",
    "analysis_reflex"           : "blue",
    "fact_check_reflex"         : "blue",
    "rule_zero_reflex"          : "blue",

    # Memory / recall reflexes → violet plane
    "memory_reflex"             : "violet",
    "recall_reflex"             : "violet",
    "anchor_reflex"             : "violet",

    # Learning reflexes → green plane
    "learning_reflex"           : "green",
    "adaptation_reflex"         : "green",
    "weight_update_reflex"      : "green",

    # Attention / focus reflexes → yellow plane
    "attention_reflex"          : "yellow",
    "focus_reflex"              : "yellow",
    "priority_reflex"           : "yellow",

    # Alert / correction reflexes → red plane
    "drift_correction_reflex"   : "red",
    "error_reflex"              : "red",
    "contradiction_reflex"      : "red",

    # Default — unknown reflex → gray plane (NOW line)
    "__default__"               : "gray",
}


def get_plane_for_reflex(reflex_name: str) -> dict:
    """
    Given a reflex name, return its full dimensional signature.
    
    Returns:
        {
          "plane_name": str,
          "color_plane": [R, G, B],
          "frequency": float,
          "hue_shift": float   # starts at 0.0 — modified by activation history
        }
    """
    plane_name = REFLEX_PLANE_MAP.get(reflex_name, REFLEX_PLANE_MAP["__default__"])
    R, G, B, freq = COLOR_PLANES[plane_name]
    return {
        "plane_name"  : plane_name,
        "color_plane" : [R, G, B],
        "frequency"   : freq,
        "hue_shift"   : 0.0,   # neutral start — shifts with use
    }


def make_reflex_entry(reflex_name: str,
                      q_state: int = WHITE,
                      hue_shift: float = 0.0,
                      extra: dict = None) -> dict:
    """
    Create a V2 dimensional reflex log entry.
    
    Use this everywhere a reflex event is logged.
    Drop-in replacement for the old flat {"reflex": name} entries.
    
    Args:
        reflex_name : the reflex identifier string
        q_state     : WHITE (+1) if firing into superposition,
                      GRAY  (0)  if firing at the NOW line,
                      BLACK (-1) if logging a sealed/collapsed result
        hue_shift   : ± shift from center frequency of the plane
                      positive = moving toward WHITE pole
                      negative = moving toward BLACK pole
        extra       : any additional fields to include
    
    Returns:
        Full dimensional reflex entry dict
    """
    plane = get_plane_for_reflex(reflex_name)
    entry = {
        "reflex"      : reflex_name,
        "plane_name"  : plane["plane_name"],
        "color_plane" : plane["color_plane"],
        "frequency"   : plane["frequency"] + hue_shift,  # shifted freq
        "hue_shift"   : hue_shift,
        "q_state"     : q_state,
        "timestamp"   : datetime.utcnow().isoformat(),
    }
    if extra:
        entry.update(extra)
    return entry


# ── Upgrade existing V1 log files ────────────────────────────────────────────

def upgrade_reflex_log(log_path: Path) -> int:
    """
    Upgrade an existing V1 reflex log file in place.
    Adds color_plane, frequency, hue_shift, q_state to entries that lack them.
    
    Returns: count of entries upgraded
    """
    if not log_path.exists():
        print(f"  [SKIP] Not found: {log_path}")
        return 0

    # Handle both JSON array files and JSONL files
    raw = log_path.read_text(encoding="utf-8").strip()
    entries = []
    is_jsonl = False

    try:
        entries = json.loads(raw)
        if not isinstance(entries, list):
            entries = [entries]
    except json.JSONDecodeError:
        # Try JSONL
        is_jsonl = True
        entries = []
        for line in raw.splitlines():
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except Exception:
                    pass

    upgraded = 0
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        reflex = entry.get("reflex")
        if not reflex:
            continue
        # Only upgrade if missing dimensional fields
        if "color_plane" not in entry:
            plane = get_plane_for_reflex(reflex)
            entry["plane_name"]  = plane["plane_name"]
            entry["color_plane"] = plane["color_plane"]
            entry["frequency"]   = plane["frequency"]
            entry["hue_shift"]   = 0.0
            entry["q_state"]     = entry.get("q_state", WHITE)
            upgraded += 1

    # Write back
    if is_jsonl:
        log_path.write_text(
            "\n".join(json.dumps(e) for e in entries) + "\n",
            encoding="utf-8"
        )
    else:
        log_path.write_text(
            json.dumps(entries, indent=2),
            encoding="utf-8"
        )

    return upgraded


def upgrade_weight_log(weight_path: Path) -> int:
    """
    Upgrade the reflex weight map to be plane-aware.
    
    Before: {"curiosity_reflex": 0.234}
    After:  {"curiosity_reflex": {"weight": 0.234, "plane": "orange", 
                                   "color_plane": [255,140,0], "frequency": 520.0}}
    """
    if not weight_path.exists():
        print(f"  [SKIP] Not found: {weight_path}")
        return 0

    data = json.loads(weight_path.read_text())
    if not isinstance(data, dict):
        return 0

    upgraded = 0
    new_data = {}
    for reflex, value in data.items():
        if isinstance(value, dict) and "weight" in value:
            new_data[reflex] = value  # already upgraded
        else:
            plane = get_plane_for_reflex(reflex)
            new_data[reflex] = {
                "weight"      : float(value) if value else 0.0,
                "plane_name"  : plane["plane_name"],
                "color_plane" : plane["color_plane"],
                "frequency"   : plane["frequency"],
                "hue_shift"   : 0.0,
            }
            upgraded += 1

    weight_path.write_text(json.dumps(new_data, indent=2))
    return upgraded


# ── V2 Correction Engine (dimensional) ───────────────────────────────────────

def dimensional_correction(weight_map: dict,
                            drift_entries: list,
                            correction_factor: float = 0.5) -> list:
    """
    V2 version of reflex_correction_engine logic.
    
    Corrects weights ONLY within the plane that drifted.
    Other planes for the same reflex are untouched.
    
    This is the key upgrade:
      V1: curiosity_reflex drifts → ALL curiosity weight reduced
      V2: curiosity_reflex drifts in orange plane → ONLY orange plane reduced
          blue plane curiosity (calm analysis) stays intact
    """
    corrections = []

    for entry in drift_entries:
        reflex = entry.get("reflex")
        drift  = entry.get("drift", 0.0)
        plane  = entry.get("plane_name") or get_plane_for_reflex(reflex)["plane_name"]

        if abs(drift) < 0.1:
            continue
        if reflex not in weight_map:
            continue

        w = weight_map[reflex]
        # Handle both old flat format and new dict format
        if isinstance(w, dict):
            # Only correct if same plane
            if w.get("plane_name") != plane:
                continue
            old_weight = w["weight"]
            correction = -drift * correction_factor
            new_weight = round(old_weight + correction, 3)
            weight_map[reflex]["weight"]     = new_weight
            weight_map[reflex]["hue_shift"]  = round(
                w.get("hue_shift", 0.0) + drift * 0.1, 4
            )
        else:
            old_weight = float(w)
            correction = -drift * correction_factor
            new_weight = round(old_weight + correction, 3)
            weight_map[reflex] = new_weight

        corrections.append({
            "timestamp"          : datetime.utcnow().isoformat(),
            "reflex"             : reflex,
            "plane_corrected"    : plane,
            "old_weight"         : old_weight,
            "drift"              : drift,
            "correction_applied" : correction,
            "new_weight"         : new_weight,
        })

        print(f"  [V2 CORRECT] {reflex} [{plane}] "
              f"{old_weight} → {new_weight}  (drift={drift})")

    return corrections


# ── Main: run upgrade on existing files ──────────────────────────────────────

def main():
    # Locate ai-core memory directory
    candidates = [
        Path("/home/comanderanch/ai-core/memory"),
        Path("memory"),
    ]
    mem_dir = None
    for c in candidates:
        if c.exists():
            mem_dir = c
            break

    if not mem_dir:
        print("❌ Could not find memory directory.")
        print("   Run from ~/ai-core/ or pass memory path.")
        sys.exit(1)

    print("=" * 60)
    print("AIA V2.00.1 — Dimensional Reflex Upgrade")
    print(f"Memory dir: {mem_dir}")
    print("=" * 60)
    print()

    # Upgrade reflex log files
    log_files = [
        mem_dir / "reflex_response_log.json",
        mem_dir / "reflex_drift_log.json",
        mem_dir / "reflex_weight_adjustments.json",
    ]
    for lf in log_files:
        count = upgrade_reflex_log(lf)
        if count > 0:
            print(f"  [UPGRADED] {lf.name} — {count} entries upgraded")
        else:
            print(f"  [CLEAN]    {lf.name}")

    print()

    # Upgrade weight map
    weight_file = mem_dir / "reflex_weight_log.json"
    count = upgrade_weight_log(weight_file)
    if count > 0:
        print(f"  [UPGRADED] {weight_file.name} — {count} weights upgraded to dimensional format")
    else:
        print(f"  [CLEAN]    {weight_file.name}")

    print()
    print("=" * 60)
    print("✅ Upgrade complete.")
    print()
    print("Color plane assignments:")
    for reflex, plane in sorted(REFLEX_PLANE_MAP.items()):
        if reflex == "__default__":
            continue
        R, G, B, freq = COLOR_PLANES[plane]
        print(f"  {reflex:<35} → {plane:<8} ({freq}hz) RGB({R},{G},{B})")
    print()
    print("  Any unregistered reflex → gray plane (400hz) — the NOW line")
    print("=" * 60)
    print()
    print("Next step:")
    print("  Add new reflexes to REFLEX_PLANE_MAP at top of this file")
    print("  as you discover them in the scripts.")
    print("  Each reflex needs a home frequency. That IS the dimensional wiring.")
    print()
    print("Delta Phase Warthog 💙🐗")


if __name__ == "__main__":
    main()
