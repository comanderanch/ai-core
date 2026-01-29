#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append('/home/comanderanch/ai-core')

from distributed_consciousness.workers.logic_worker import LogicWorker
import time

print("⚡ Starting Logic Worker...")

worker = LogicWorker(
    worker_id="logic_001",
    field_path="/home/comanderanch/ai-core/consciousness_data/field/em_field_substrate.npy"
)

print("✅ Logic Worker running")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n👋 Stopped")
