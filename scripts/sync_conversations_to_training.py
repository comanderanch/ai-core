#!/usr/bin/env python3
"""
Sync EM/Emotion conversation history to training data
Extracts user_input + synthesis from JSON sessions
Writes to user_comm_qa.txt for weight training
"""

import json
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
CONV_DIR = BASE / "consciousness_data" / "conversations"
QA_FILE = BASE / "training_data" / "user_comm_qa.txt"

def extract_qa_from_session(session_file):
    """Extract Q&A pairs from a session JSON"""
    pairs = []
    
    try:
        with open(session_file, 'r') as f:
            data = json.load(f)
        
        for entry in data:
            user_input = entry.get('user_input', '').strip()
            synthesis = entry.get('synthesis', '').strip()
            
            if user_input and synthesis:
                pairs.append((user_input, synthesis))
    
    except Exception as e:
        print(f"Error reading {session_file.name}: {e}")
    
    return pairs

def get_existing_questions():
    """Get questions already in training data"""
    existing = set()
    
    if QA_FILE.exists():
        with open(QA_FILE, 'r') as f:
            for line in f:
                if '|' in line:
                    q = line.split('|')[0].strip().lower()
                    existing.add(q)
    
    return existing

def sync_conversations():
    """Sync all conversation history to training data"""
    
    if not CONV_DIR.exists():
        print(f"No conversations directory: {CONV_DIR}")
        return
    
    print("🔄 Syncing conversation history to training data...")
    print()
    
    # Get existing questions (avoid duplicates)
    existing = get_existing_questions()
    print(f"  Existing Q&A pairs: {len(existing)}")
    
    # Extract from all session files
    all_pairs = []
    session_files = sorted(CONV_DIR.glob("session_*.json"))
    
    print(f"  Session files found: {len(session_files)}")
    print()
    
    for session_file in session_files:
        pairs = extract_qa_from_session(session_file)
        all_pairs.extend(pairs)
    
    # Filter out duplicates
    new_pairs = []
    for q, a in all_pairs:
        if q.lower() not in existing:
            new_pairs.append((q, a))
            existing.add(q.lower())
    
    print(f"  New unique Q&A pairs: {len(new_pairs)}")
    
    if not new_pairs:
        print("  ✅ Already up to date!")
        return
    
    # Append to training file
    with open(QA_FILE, 'a') as f:
        for q, a in new_pairs:
            f.write(f"{q} | {a}\n")
    
    print(f"  ✅ Added {len(new_pairs)} pairs to training data")
    print()
    print(f"Total Q&A pairs now: {len(existing)}")

if __name__ == "__main__":
    sync_conversations()
