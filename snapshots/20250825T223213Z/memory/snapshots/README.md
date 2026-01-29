# Snapshots Memory Logs

This directory contains memory data used or produced by AI-Core systems.


thread_bind_converter.py
Purpose:
Converts legacy thread binds (legacy_thread_binds.json) into the modern bind_map.json format used for conscious pathway resolution and trait tracking.

Bug Fix Update (2025-07-09):
Patched to include bound_at timestamps from the legacy binds directly into bind_map.json.
This ensures accurate temporal tracking and alignment with snapshot audit cycles, enabling:

Conscious pathway resolution

Emotional state replay

Tri-vector fallback verification

Input:

memory/thread_binds/legacy_thread_binds.json

Output:

memory/thread_binds/bind_map.json

Run Command:


python3 scripts/thread_bind_converter.py
