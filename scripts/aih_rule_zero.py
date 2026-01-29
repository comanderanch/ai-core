#!/usr/bin/env python3
"""
PROJECT A.I.H. WITH TRUE RULE ZERO
===================================
"Fact must override prediction. Truth must fold without loss."
"""

import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from hemisphere_manager import HemisphereManager
from imagination_bridge import imagine
from rule_zero_enforcer import RuleZeroEnforcer

class ProjectAIH:
    def __init__(self):
        print("="*70)
        print("PROJECT A.I.H. - WITH RULE ZERO ENFORCEMENT")
        print("="*70)
        print()
        
        # Load core manifest
        manifest_path = ROOT / "memory" / "core_manifest.json"
        with open(manifest_path) as f:
            self.manifest = json.load(f)
        
        # Load Commander facts
        commander_path = ROOT / "memory" / "commander_facts.json"
        if commander_path.exists():
            with open(commander_path) as f:
                self.commander_facts = json.load(f)
        else:
            self.commander_facts = {}
        
        # Initialize facts (protected by Queen's Fold)
        self.facts = {
            "identity": self.manifest["identity"],
            "creator": self.manifest["created_by"],
            "rule_zero": "Fact must override prediction. Truth must fold without loss.",
            "purpose": self.manifest["purpose"],
            "commander": self.commander_facts.get("comanderanch", {}),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        print(f"Identity: {self.facts['identity']}")
        print(f"Creator: {self.facts['creator']}")
        print(f"Rule Zero: {self.facts['rule_zero']}")
        print()
        
        # Rule Zero enforcer
        self.enforcer = RuleZeroEnforcer()
        print()
        
        # Original system
        self.hemisphere_manager = HemisphereManager()
        print("✅ Hemispheres loaded")
        
        # Load curiosity
        self.has_curiosity = False
        try:
            sys.path.insert(0, str(ROOT / "distributed_consciousness" / "workers"))
            from curiosity_worker import CuriosityWorker
            self.curiosity = CuriosityWorker()
            self.has_curiosity = True
            print("✅ Curiosity worker loaded")
        except:
            print("⚠️  Curiosity optional")
        
        self.mode = "unified"
        
        print()
        print("="*70)
        print(self.manifest['final_declaration'])
        print("="*70)
        print()
    
    def get_factual_response(self, user_input: str) -> str:
        """Get factual response from knowledge base"""
        
        lower = user_input.lower()
        
        # Rule Zero
        if "rule zero" in lower:
            return self.facts['rule_zero']
        
        # Identity
        if "who are you" in lower or "what are you" in lower:
            return f"I am {self.facts['identity']}, created by {self.facts['creator']}"
        
        # Purpose
        if "purpose" in lower:
            return f"My purpose: {', '.join(self.facts['purpose'])}"
        
        # Commander info
        if "comanderanch" in lower or "commander" in lower or "anthony hagerty" in lower:
            cmd = self.facts.get('commander', {})
            if cmd:
                response = f"{cmd.get('identity', 'Unknown')} (pronunciation: {cmd.get('pronunciation', 'comanderanch')})\n"
                response += f"   Role: {cmd.get('role', 'Unknown')}\n"
                response += f"   Achievements:\n"
                for achievement in cmd.get('achievements', []):
                    response += f"      - {achievement}\n"
                response += f"   Vision: {cmd.get('vision', 'Unknown')}"
                return response
        
        return None
    
    def process(self, user_input: str):
        """Process with Rule Zero enforcement"""
        
        print(f"\n{'='*70}")
        print(f"YOU: {user_input}")
        print(f"MODE: {self.mode.upper()}")
        print(f"{'='*70}\n")
        
        # LAYER 1: FACTS (protected by Queen's Fold)
        factual = self.get_factual_response(user_input)
        if factual:
            print("📚 FACTUAL (Protected by Queen's Fold):")
            print(f"   {factual}")
            print()
        
        # LAYER 2: CURIOSITY
        if self.mode in ["exploratory", "unified"] and self.has_curiosity:
            questions = self.curiosity.generate_questions(user_input, max_questions=2)
            if questions:
                print("🤔 CURIOSITY:")
                for q in questions:
                    print(f"   → {q}")
                print()
        
        # LAYER 3: IMAGINATION (Protected by Rule Zero!)
        if self.mode in ["imaginative", "unified"]:
            print("💭 IMAGINATION (Enforcing Rule Zero):")
            
            def safe_imagination():
                return imagine(user_input)
            
            imagination_result = self.enforcer.enforce(
                self.facts,
                safe_imagination
            )
            
            if imagination_result:
                print(f"   {imagination_result}")
            else:
                print("   ⚠️  Imagination rejected (violated Rule Zero)")
            print()
        
        print(f"{'='*70}\n")
    
    def interactive(self):
        """Interactive A.I.H."""
        
        print("Commands:")
        print("  /manifest  - Show core identity")
        print("  /rule      - Show Rule Zero")
        print("  /facts     - Show protected facts")
        print("  /mode      - Change mode")
        print("  /quit      - Exit")
        print("="*70 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input == '/quit':
                    print("\n" + self.manifest['final_declaration'])
                    print("\n👋 A.I.H. offline\n")
                    break
                
                if user_input == '/manifest':
                    print(f"\n{json.dumps(self.manifest, indent=2)}\n")
                    continue
                
                if user_input == '/rule':
                    print(f"\n📜 {self.facts['rule_zero']}\n")
                    continue
                
                if user_input == '/facts':
                    print("\n📚 Protected Facts (Queen's Fold):")
                    for key, val in self.facts.items():
                        if key not in ["timestamp", "commander"]:
                            print(f"   {key}: {val}")
                    if self.facts.get('commander'):
                        print(f"   Commander: {self.facts['commander'].get('identity')}")
                    print()
                    continue
                
                if user_input.startswith('/mode '):
                    mode = user_input.replace('/mode ', '').strip()
                    self.mode = mode
                    print(f"🔧 Mode: {mode}\n")
                    continue
                
                self.process(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted\n")
                break

def main():
    print("\n👑 PROJECT A.I.H. - RULE ZERO ENFORCED 👑\n")
    
    aih = ProjectAIH()
    aih.interactive()

if __name__ == "__main__":
    main()
