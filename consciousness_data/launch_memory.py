#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append('/home/comanderanch/ai-core')

from distributed_consciousness.workers.memory_worker import MemoryWorker
import time

print("🧠 Starting Memory Worker...")

worker = MemoryWorker(
    worker_id="memory_001",
    memory_path="/home/comanderanch/ai-core/consciousness_data/memory/memories.json",
    field_path="/home/comanderanch/ai-core/consciousness_data/field/em_field_substrate.npy"
)

print("✅ Memory Worker running")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n👋 Stopped")
