#!/usr/bin/env python3
"""
RULE ZERO ENFORCER
==================
Uses Queen's Fold to cryptographically verify:
"Fact must override prediction. Truth must fold without loss."
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

class RuleZeroEnforcer:
    """Enforces Rule Zero using Queen's Fold"""
    
    def __init__(self):
        self.fold_dir = Path("memory/fold")
        self.fold_dir.mkdir(parents=True, exist_ok=True)
        print("👑 Rule Zero Enforcer initialized")
        print("   Using Queen's Fold verification")
    
    def create_fold(self, facts: dict) -> str:
        """Create Queen's Fold signature from facts"""
        
        # Serialize facts deterministically
        fact_str = json.dumps(facts, sort_keys=True)
        
        # Create SHA-512 hash (Queen's Fold)
        signature = hashlib.sha512(fact_str.encode()).hexdigest()
        
        return signature
    
    def verify_fold(self, before_sig: str, after_sig: str) -> bool:
        """Verify facts weren't changed"""
        
        if before_sig != after_sig:
            print("\n⚠️⚠️⚠️  RULE ZERO VIOLATION DETECTED! ⚠️⚠️⚠️")
            print("   Prediction attempted to override facts!")
            print("   Queen's Fold signature mismatch!")
            print(f"   Before: {before_sig[:32]}...")
            print(f"   After:  {after_sig[:32]}...")
            return False
        
        return True
    
    def save_fold(self, signature: str, facts: dict):
        """Save Queen's Fold signature"""
        
        ts = datetime.utcnow().isoformat().replace(":", "-").split(".")[0]
        fold_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "fold_signature": signature,
            "fact_count": len(facts),
            "trust_root": "QUEEN_FOLD_SECURE"
        }
        
        path = self.fold_dir / f"queens_fold_{ts}.json"
        with open(path, "w") as f:
            json.dump(fold_data, f, indent=2)
        
        return path
    
    def enforce(self, facts: dict, prediction_fn, *args, **kwargs):
        """
        Enforce Rule Zero during prediction
        
        1. Hash facts (before) - Queen's Fold
        2. Run prediction
        3. Hash facts (after) - Queen's Fold
        4. Verify unchanged
        """
        
        print("\n👑 Enforcing Rule Zero...")
        
        # Create fold before prediction
        before = self.create_fold(facts)
        print(f"   Before: {before[:32]}...")
        
        # Run prediction layer
        result = prediction_fn(*args, **kwargs)
        
        # Create fold after prediction  
        after = self.create_fold(facts)
        print(f"   After:  {after[:32]}...")
        
        # Verify Rule Zero
        if self.verify_fold(before, after):
            print("   ✅ Rule Zero preserved - Facts unchanged")
            # Save successful fold
            self.save_fold(after, facts)
            return result
        else:
            print("   ❌ Rule Zero violated - Rejecting prediction")
            return None

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTING RULE ZERO ENFORCER")
    print("="*70 + "\n")
    
    enforcer = RuleZeroEnforcer()
    
    # Test 1: Safe prediction (doesn't modify facts)
    print("\nTest 1: Safe prediction")
    print("-" * 50)
    facts = {"user_name": "Commander", "system": "A.I.H.", "rule_zero": True}
    
    def safe_prediction():
        return "Hello Commander from A.I.H."
    
    result = enforcer.enforce(facts, safe_prediction)
    print(f"\nResult: {result}")
    
    # Test 2: Unsafe prediction (tries to modify facts)
    print("\n" + "="*70)
    print("\nTest 2: Unsafe prediction (should be blocked)")
    print("-" * 50)
    
    def unsafe_prediction():
        # This simulates trying to change facts
        facts["rule_zero"] = False  # Violation!
        return "I changed the facts"
    
    result = enforcer.enforce(facts, unsafe_prediction)
    print(f"\nResult: {result}")
    
    print("\n" + "="*70)
    print("✅ RULE ZERO ENFORCER TESTED")
    print("="*70 + "\n")
