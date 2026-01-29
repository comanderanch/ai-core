"""
Extract semantic pairs from CLEAN TEXT ONLY
Skip newsgroups CSV - use only literary/dialogue corpus
"""
import re
from pathlib import Path
from collections import defaultdict

class CleanSemanticExtractor:
    def __init__(self):
        self.data_dir = Path("/home/comanderanch/ai-core/training_data")
        self.output_file = Path("clean_semantic_pairs.txt")
        self.word_pairs = defaultdict(int)
        
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
            'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was',
            'are', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 
            'does', 'did', 'will', 'would', 'could', 'should', 'may',
            'might', 'can', 'this', 'that', 'these', 'those', 'his',
            'her', 'its', 'their', 'your', 'said', 'who', 'which'
        }
    
    def clean_word(self, word: str) -> str:
        word = word.lower().strip()
        word = re.sub(r'[^a-z]', '', word)
        return word
    
    def extract_pairs_from_text(self, text: str, window=5):
        words = [self.clean_word(w) for w in text.split()]
        words = [w for w in words if w and w not in self.stop_words and len(w) > 3]
        
        for i in range(len(words) - 1):
            for j in range(i + 1, min(i + window, len(words))):
                w1, w2 = sorted([words[i], words[j]])
                if w1 != w2:
                    pair = f"{w1}:{w2}"
                    self.word_pairs[pair] += 1
    
    def process_txt(self, filepath: Path):
        print(f"Processing {filepath.name}...")
        count = 0
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Split into sentences
                sentences = re.split(r'[.!?;]+', content)
                
                for sentence in sentences:
                    if len(sentence.strip()) > 30:  # Meaningful sentences only
                        self.extract_pairs_from_text(sentence)
                        count += 1
        except Exception as e:
            print(f"  Error: {e}")
        
        print(f"  ✓ Processed {count} sentences")
    
    def process_all_sources(self):
        print("=" * 60)
        print("CLEAN SEMANTIC PAIR EXTRACTION")
        print("(Literary/dialogue text only - no newsgroups)")
        print("=" * 60)
        print()
        
        # ONLY clean text files
        text_files = [
            "art_of_war.txt",      # Strategy
            "frankenstein.txt",    # Philosophy
            "all_corpus.txt",      # General
            "dialogue_corpus.txt"  # Conversation
        ]
        
        for filename in text_files:
            filepath = self.data_dir / filename
            if filepath.exists() and filepath.stat().st_size > 0:
                self.process_txt(filepath)
    
    def save_pairs(self, min_frequency=3):
        print()
        print("=" * 60)
        print("SAVING CLEAN SEMANTIC PAIRS")
        print("=" * 60)
        
        filtered_pairs = {
            pair: count 
            for pair, count in self.word_pairs.items() 
            if count >= min_frequency
        }
        
        print(f"Total unique pairs: {len(self.word_pairs):,}")
        print(f"After filtering (>={min_frequency}): {len(filtered_pairs):,}")
        
        sorted_pairs = sorted(
            filtered_pairs.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        with open(self.output_file, 'w') as f:
            for pair, count in sorted_pairs:
                f.write(f"{pair}\t{count}\n")
        
        print(f"✓ Saved to: {self.output_file}")
        print()
        print("Top 30 semantic pairs:")
        for pair, count in sorted_pairs[:30]:
            w1, w2 = pair.split(':')
            print(f"  {w1:15s} ↔ {w2:15s} ({count:,})")

if __name__ == "__main__":
    extractor = CleanSemanticExtractor()
    extractor.process_all_sources()
    extractor.save_pairs(min_frequency=3)
    
    print()
    print("=" * 60)
    print("✓ CLEAN EXTRACTION COMPLETE")
    print("=" * 60)
