# tests/test_llm_interaction.py
# Phase 38 – Verification Suite for Hemisphere LLM Interface
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import unittest
from hemisphere_manager import HemisphereManager
from llm_output_resolver import LLMOutputResolver
from drift_switcher import DriftSwitcher
import json

class TestLLMInteraction(unittest.TestCase):

    def setUp(self):
        self.hm = HemisphereManager()
        self.resolver = LLMOutputResolver()
        self.switcher = DriftSwitcher()

    def test_hemisphere_switch(self):
        original = self.hm.get_current_hemisphere()
        self.hm.switch_hemisphere()
        switched = self.hm.get_current_hemisphere()
        self.assertNotEqual(original, switched)

    def test_token_load(self):
        tokens = self.hm.get_active_tokens()
        self.assertIsInstance(tokens, list)

    def test_output_resolver_structure(self):
        result = self.resolver.resolve_outputs()
        self.assertIn("output_left", result)
        self.assertIn("output_right", result)
        self.assertIn("drift_detected", result)

    def test_drift_switch_log(self):
        self.switcher.run_check()
        path = "memory/snapshots/drift_switch_log.json"
        with open(path, "r") as f:
            log = json.load(f)
        self.assertIsInstance(log, list)
        self.assertIn("drift_detected", log[-1])

if __name__ == '__main__':
    unittest.main()
