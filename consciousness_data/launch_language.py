#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append('/home/comanderanch/ai-core')

from distributed_consciousness.workers.language_worker import LanguageWorker
import time

print("🔥 Starting Language Worker...")

worker = LanguageWorker(
    worker_id="language_001",
    field_path="/home/comanderanch/ai-core/consciousness_data/field/em_field_substrate.npy"
)

print("✅ Language Worker running")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n👋 Stopped")
