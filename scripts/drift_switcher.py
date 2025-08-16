# drift_switcher.py
# Phase 38.3 – Automatically switches active hemisphere on output drift
from hemisphere_manager import HemisphereManager
from llm_output_resolver import LLMOutputResolver
from datetime import datetime
from pathlib import Path
import json, time

class DriftSwitcher:
    def __init__(self):
        self.hm = HemisphereManager()
        self.resolver = LLMOutputResolver()
        self.log_path = Path("memory/snapshots/drift_switch_log.json")

    def run_check(self):
        result = self.resolver.resolve_outputs()

        log_entry = {
            "timestamp": result["timestamp"],
            "active_hemisphere": result["active_hemisphere"],
            "drift_detected": result["drift_detected"],
            "switched": False,
            "new_active_hemisphere": result["active_hemisphere"]
        }

        if result["drift_detected"]:
            self.hm.switch_hemisphere()
            log_entry["switched"] = True
            log_entry["new_active_hemisphere"] = self.hm.get_current_hemisphere()

        self._append_log(self.log_path, log_entry)

        if log_entry["switched"]:
            print(f"[↺] Drift detected. Hemisphere switched to {log_entry['new_active_hemisphere'].upper()}.")
        else:
            print(f"[✓] No drift. Staying on {log_entry['active_hemisphere'].upper()}.")

    @staticmethod
    def _append_log(path: Path, entry: dict):
        log = []
        if path.exists():
            try:
                log = json.loads(path.read_text())
            except json.JSONDecodeError:
                log = []
        log.append(entry)
        path.write_text(json.dumps(log, indent=2))


# ------------------------------
# New: pure-function drift decide
# ------------------------------
_DRIFT_EVENTS = Path("memory/drift/drift_events.json")
_DRIFT_EVENTS.parent.mkdir(parents=True, exist_ok=True)
if not _DRIFT_EVENTS.exists():
    _DRIFT_EVENTS.write_text("[]")

def _tok(s: str):
    return [w.lower() for w in s.split() if w.strip()]

def _jaccard(a, b):
    A, B = set(a), set(b)
    if not A and not B:
        return 1.0
    return len(A & B) / max(1, len(A | B))

def _lev_dist(a, b):
    # token-level Levenshtein distance
    n, m = len(a), len(b)
    if n == 0: return m
    if m == 0: return n
    dp = list(range(m+1))
    for i in range(1, n+1):
        prev, dp[0] = dp[0], i
        for j in range(1, m+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            prev, dp[j] = dp[j], min(dp[j] + 1, dp[j-1] + 1, prev + cost)
    return dp[m]

def decide(reply_left: str, reply_right: str, evidence_hint: str = "") -> dict:
    """
    Compare two candidate replies and choose which hemisphere to trust.
    Logs to memory/drift/drift_events.json. Does NOT switch hemispheres itself.
    Returns: {"chosen": "left"|"right", "metrics": {"jaccard":..,"lev_sim":..}, ...}
    """
    tl, tr = _tok(reply_left), _tok(reply_right)
    jac = _jaccard(tl, tr)
    dist = _lev_dist(tl, tr)
    norm = max(len(tl), len(tr), 1)
    lev_sim = 1.0 - (dist / norm)

    # Agreement ⇒ prefer LEFT; disagreement ⇒ prefer RIGHT (raw).
    score_left = 0.6 * jac + 0.4 * lev_sim
    chosen = "left" if score_left >= 0.5 else "right"

    event = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "reply_left": reply_left,
        "reply_right": reply_right,
        "metrics": {"jaccard": round(jac, 4), "lev_sim": round(lev_sim, 4)},
        "chosen": chosen,
        "evidence_hint": evidence_hint
    }

    # append capped log
    try:
        log = json.loads(_DRIFT_EVENTS.read_text())
    except Exception:
        log = []
    log.append(event)
    if len(log) > 1000:
        log = log[-1000:]
    _DRIFT_EVENTS.write_text(json.dumps(log, indent=2))

    return event


if __name__ == "__main__":
    # Preserve your original CLI behavior (class-based check)
    switcher = DriftSwitcher()
    switcher.run_check()
