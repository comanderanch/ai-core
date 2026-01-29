#!/usr/bin/env python3
"""
Extract emotion/psychology semantic pairs from texts.

Focuses on emotional concepts, mental states, psychological terms.
"""

import re
from collections import defaultdict
from pathlib import Path

def clean_text(text):
    """Clean and normalize text."""
    # Remove special characters, keep only words
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    # Lowercase
    text = text.lower()
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def extract_emotion_pairs(text_file, output_file):
    """
    Extract semantic pairs focused on psychology/emotion.
    
    Looks for co-occurrences of psychological terms within same context window.
    """
    print(f"Processing: {text_file}")
    
    # Load text
    with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    # Clean
    text = clean_text(text)
    words = text.split()
    
    print(f"  Total words: {len(words):,}")
    
    # Psychology/emotion keywords to focus on
    emotion_keywords = {
        # Emotions
        'anger', 'angry', 'rage', 'furious', 'mad', 'frustrated', 'annoyed',
        'fear', 'afraid', 'scared', 'anxious', 'worried', 'nervous', 'panic',
        'sadness', 'sad', 'depressed', 'grief', 'sorrow', 'melancholy', 'unhappy',
        'joy', 'happy', 'happiness', 'excited', 'pleased', 'delighted', 'glad',
        'love', 'affection', 'caring', 'compassion', 'empathy', 'kindness',
        'disgust', 'revulsion', 'aversion', 'contempt',
        'surprise', 'amazement', 'astonishment', 'shock',
        
        # Mental states
        'thinking', 'thought', 'cognition', 'reasoning', 'logic', 'rational',
        'feeling', 'emotion', 'affect', 'mood', 'sentiment',
        'consciousness', 'awareness', 'attention', 'perception', 'sensation',
        'memory', 'recall', 'remembering', 'forgetting', 'recognition',
        'learning', 'understanding', 'comprehension', 'knowledge',
        'decision', 'choice', 'judgment', 'evaluation',
        
        # Psychological concepts
        'behavior', 'action', 'response', 'reaction', 'reflex',
        'motivation', 'drive', 'desire', 'want', 'need',
        'personality', 'trait', 'characteristic', 'disposition',
        'stress', 'anxiety', 'tension', 'pressure', 'strain',
        'coping', 'adaptation', 'adjustment', 'resilience',
        'development', 'growth', 'maturation', 'change',
        
        # Social/relational
        'relationship', 'connection', 'bond', 'attachment',
        'communication', 'interaction', 'social', 'interpersonal',
        'trust', 'belief', 'confidence', 'faith',
        'conflict', 'disagreement', 'argument', 'dispute',
        'cooperation', 'collaboration', 'teamwork', 'helping',
        
        # Therapy/clinical
        'therapy', 'treatment', 'counseling', 'intervention',
        'disorder', 'illness', 'condition', 'syndrome',
        'diagnosis', 'assessment', 'evaluation', 'symptom',
        'recovery', 'healing', 'improvement', 'wellness'
    }
    
    # Find pairs within context window
    pairs = defaultdict(int)
    context_window = 10  # Words before/after
    
    for i, word in enumerate(words):
        if word in emotion_keywords:
            # Look at surrounding context
            start = max(0, i - context_window)
            end = min(len(words), i + context_window + 1)
            
            context = words[start:end]
            
            for other_word in context:
                if other_word != word and other_word in emotion_keywords:
                    # Create pair (sorted for consistency)
                    pair = tuple(sorted([word, other_word]))
                    pairs[pair] += 1
    
    print(f"  Found {len(pairs):,} unique pairs")
    
    # Filter by frequency (at least 2 occurrences)
    filtered_pairs = [(w1, w2, count) for (w1, w2), count in pairs.items() if count >= 2]
    filtered_pairs.sort(key=lambda x: x[2], reverse=True)
    
    print(f"  After filtering: {len(filtered_pairs):,} pairs")
    
    # Save
    with open(output_file, 'w') as f:
        for w1, w2, count in filtered_pairs:
            f.write(f"{w1}\t{w2}\t{count}\n")
    
    print(f"  Saved to: {output_file}")
    
    return len(filtered_pairs)

def main():
    print("="*70)
    print("EXTRACTING PSYCHOLOGY/EMOTION SEMANTIC PAIRS")
    print("="*70)
    print()
    
    # Process both psychology texts
    texts = [
        ("training_data/psychology_books/cognitive_sciences.txt", 
         "training_data/psychology_pairs_cognitive.txt"),
        ("training_data/psychology_books/psychology_book.txt",
         "training_data/psychology_pairs_book.txt")
    ]
    
    total_pairs = 0
    
    for text_file, output_file in texts:
        if Path(text_file).exists():
            count = extract_emotion_pairs(text_file, output_file)
            total_pairs += count
        else:
            print(f"⚠️  File not found: {text_file}")
        print()
    
    print("="*70)
    print(f"✅ EXTRACTION COMPLETE")
    print(f"   Total semantic pairs: {total_pairs:,}")
    print("="*70)
    
    # Show sample pairs
    print("\nSample pairs from psychology book:")
    with open("training_data/psychology_pairs_book.txt", 'r') as f:
        for i, line in enumerate(f):
            if i >= 20:
                break
            w1, w2, count = line.strip().split('\t')
            print(f"  {w1:20} ↔ {w2:20} ({count} times)")

if __name__ == "__main__":
    main()
