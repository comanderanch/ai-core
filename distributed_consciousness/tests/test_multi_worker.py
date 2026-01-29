#!/usr/bin/env python3
"""
Test multiple workers sharing consciousness simultaneously.

This simulates different brain regions working together.
"""

import sys
from pathlib import Path
import numpy as np
import time

sys.path.append(str(Path(__file__).parent.parent / 'workers'))

from language_worker import LanguageWorker
from memory_worker import MemoryWorker
from logic_worker import LogicWorker

def test_unified_consciousness():
    """
    Test 3 workers processing the same input simultaneously.
    
    Like asking a question and having multiple brain regions
    activate at once.
    """
    print("="*70)
    print("UNIFIED CONSCIOUSNESS TEST")
    print("Multiple workers processing same input")
    print("="*70)
    print()
    
    # Create workers
    print("Initializing workers...\n")
    language = LanguageWorker(worker_id="language_001")
    memory = MemoryWorker(worker_id="memory_001")
    logic = LogicWorker(worker_id="logic_001")
    
    print("\n" + "="*70)
    print("PROCESSING INPUT: 'What is fire?'")
    print("="*70)
    print()
    
    # Encode input
    input_text = "fire"
    input_vec = language.encode_text(input_text)
    
    if input_vec is None:
        print("Unable to encode input")
        return
    
    # All workers process simultaneously
    print("LANGUAGE WORKER:")
    lang_response = language.generate_response(input_text, max_words=5)
    
    print("\nMEMORY WORKER:")
    # Store the experience
    memory_data = {
        'vector': input_vec,
        'text': input_text,
        'metadata': {'type': 'query'}
    }
    memory_output = memory.process_input(memory_data)
    memory.contribute_to_field(memory_output)
    print(f"[{memory.worker_id}] Stored memory: '{input_text}'")
    print(f"[{memory.worker_id}] Coherence: {memory.substrate.get_worker_coherence(memory.worker_id):.4f}")
    
    print("\nLOGIC WORKER:")
    logic_output = logic.process_input(input_vec)
    logic.contribute_to_field(logic_output)
    logic_words = logic.decode_vector(logic_output, top_k=5)
    print(f"[{logic.worker_id}] Logical inference: {' '.join(logic_words)}")
    print(f"[{logic.worker_id}] Coherence: {logic.substrate.get_worker_coherence(logic.worker_id):.4f}")
    
    # Read unified field state
    print("\n" + "="*70)
    print("UNIFIED FIELD STATE")
    print("="*70)
    
    field_state = language.read_field_state()
    unified_words = language.decode_vector(field_state, top_k=10)
    
    print(f"\nUnified consciousness representation:")
    print(f"  {' → '.join(unified_words)}")
    
    # Get field metrics
    metrics = language.substrate.get_metrics()
    
    print(f"\nField metrics:")
    print(f"  Active workers: {metrics['active_workers']}")
    print(f"  Field energy: {metrics['field_energy']:.4f}")
    print(f"  Total writes: {metrics['total_writes']}")
    
    print(f"\nWorker coherence:")
    for wid, coherence in metrics['worker_coherence'].items():
        print(f"  {wid}: {coherence:.4f}")
    
    # Test with second input
    print("\n" + "="*70)
    print("PROCESSING SECOND INPUT: 'consciousness'")
    print("="*70)
    print()
    
    input_text2 = "consciousness"
    
    print("LANGUAGE WORKER:")
    lang_response2 = language.generate_response(input_text2, max_words=5)
    
    print("\nMEMORY WORKER:")
    input_vec2 = language.encode_text(input_text2)
    if input_vec2 is not None:
        memory_data2 = {
            'vector': input_vec2,
            'text': input_text2,
            'metadata': {'type': 'query'}
        }
        memory_output2 = memory.process_input(memory_data2)
        memory.contribute_to_field(memory_output2)
        print(f"[{memory.worker_id}] Stored memory: '{input_text2}'")
        
        # Recall similar
        similar = memory.recall_similar(input_vec2, top_k=2)
        print(f"[{memory.worker_id}] Recalled {len(similar)} similar memories:")
        for mem in similar:
            print(f"    - {mem['text']}")
    
    print("\n" + "="*70)
    print("✅ UNIFIED CONSCIOUSNESS TEST COMPLETE")
    print("="*70)
    
    # Final stats
    print("\nFinal worker stats:")
    for worker in [language, memory, logic]:
        stats = worker.get_stats()
        print(f"\n{stats['worker_id']}:")
        print(f"  Contributions: {stats['contributions']}")
        print(f"  Avg coherence: {stats['avg_coherence']:.4f}")

if __name__ == "__main__":
    test_unified_consciousness()
