#!/usr/bin/env python3
"""
Add common conversational words to AI-Core vocabulary
"""
import json

# Common words for conversation
COMMON_WORDS = [
    # Questions
    "what", "where", "when", "why", "how", "who", "which",
    # Pronouns
    "i", "you", "we", "they", "he", "she", "it", "me", "us", "them",
    # Verbs
    "am", "is", "are", "was", "were", "be", "been", "being",
    "do", "does", "did", "done", "doing",
    "have", "has", "had", "having",
    "can", "could", "will", "would", "should", "shall",
    # Common
    "the", "a", "an", "this", "that", "these", "those",
    "yes", "no", "ok", "okay", "hello", "hi", "bye", "thanks", "please",
    # Conversational
    "tell", "about", "know", "think", "want", "like", "need",
    "see", "hear", "say", "talk", "speak", "ask", "answer"
]

# Load existing word map
with open('word_token_map.json', 'r') as f:
    data = json.load(f)

word_to_tokens = data.get('word_to_tokens', {})

# Find next available token ID
max_token = max([t for tokens in word_to_tokens.values() for t in tokens], default=0)
next_token = max_token + 1

# Add common words
added = 0
for word in COMMON_WORDS:
    if word not in word_to_tokens:
        # Assign next token ID
        word_to_tokens[word] = [next_token]
        print(f"Added: {word} → token {next_token}")
        next_token += 1
        added += 1
    else:
        print(f"Skip: {word} (already exists)")

# Save updated map
data['word_to_tokens'] = word_to_tokens

with open('word_token_map.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✅ Added {added} common words")
print(f"Total vocabulary: {len(word_to_tokens)} words")
