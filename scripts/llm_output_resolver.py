# llm_output_resolver.py
# Phase 38.2 – Simulates LLM output comparison from hemispheric token sets

from hemisphere_manager import HemisphereManager
from datetime import datetime

class LLMOutputResolver:
    def __init__(self):
        self.hm = HemisphereManager()

    def simulate_llm_output(self, tokens):
        """
        Placeholder LLM output for v1.0.
        Emits a compact preview of the first few tokens to prove the loop.
        """
        if not tokens:
            return ""
        # Show up to first 6 tokens
        preview = " ".join(str(t) for t in tokens[:6])
        return preview

    def resolve_outputs(self, prefer_active=True):
        all_tokens = self.hm.get_all_tokens()
        active_hemi = self.hm.get_current_hemisphere()

        output_left  = self.simulate_llm_output(all_tokens["left"])
        output_right = self.simulate_llm_output(all_tokens["right"])

        drift_detected = (output_left != output_right)

        # v1.0 rule: ALWAYS choose something
        if drift_detected:
            chosen = output_left if active_hemi == "left" else output_right
        else:
            chosen = output_left  # same either way

        result = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "active_hemisphere": active_hemi,
            "output_left": output_left,
            "output_right": output_right,
            "drift_detected": drift_detected,
            "chosen_output": chosen
        }
        return result

# --- External API ---
def resolve_llm_output(prompt=None):
    """
    Wrapper for external modules (prompt is ignored in v1.0).
    Returns a non-empty string by always choosing an output, even on drift.
    """
    result = LLMOutputResolver().resolve_outputs()
    return result["chosen_output"] or "[no-output]"
