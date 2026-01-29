"""
AI-Core: Expanded Semantic Pair Extraction - FIXED CSV PARSING
"""
import json
import csv
import re
from pathlib import Path
from collections import defaultdict

class ExpandedSemanticExtractor:
    def __init__(self):
        self.data_dir = Path("/home/comanderanch/ai-core/training_data")
        self.output_file = Path("expanded_semantic_pairs_fixed.txt")
        self.word_pairs = defaultdict(int)
        
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
            'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was',
            'are', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 
            'does', 'did', 'will', 'would', 'could', 'should', 'may',
            'might', 'can', 'this', 'that', 'these', 'those'
        }
    
    def clean_word(self, word: str) -> str:
        word = word.lower().strip()
        word = re.sub(r'[^a-z]', '', word)
        return word
    
    def extract_pairs_from_text(self, text: str, window=3):
        words = [self.clean_word(w) for w in text.split()]
        words = [w for w in words if w and w not in self.stop_words and len(w) > 2]
        
        for i in range(len(words) - 1):
            for j in range(i + 1, min(i + window, len(words))):
                w1, w2 = sorted([words[i], words[j]])
                if w1 != w2:
                    pair = f"{w1}:{w2}"
                    self.word_pairs[pair] += 1
    
    def process_csv(self, filepath: Path):
        """Process CSV - extract ONLY text_cleaned column"""
        print(f"Processing {filepath.name}...")
        count = 0
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f, delimiter=';')
                
                for row in reader:
                    # Extract ONLY the cleaned text column
                    if 'text_cleaned' in row and row['text_cleaned']:
                        text = row['text_cleaned']
                    elif 'text' in row and row['text']:
                        # Fallback to raw text if cleaned doesn't exist
                        text = row['text']
                    else:
                        continue
                    
                    # Skip if it's metadata/headers
                    if 'From:' in text or 'Subject:' in text:
                        continue
                    
                    self.extract_pairs_from_text(text)
                    count += 1
                    
                    if count % 10000 == 0:
                        print(f"  Processed {count} rows...")
        except Exception as e:
            print(f"  Error: {e}")
        
        print(f"  ✓ Completed: {count} rows")
    
    def process_txt(self, filepath: Path):
        print(f"Processing {filepath.name}...")
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                sentences = re.split(r'[.!?]+', content)
                
                for sentence in sentences:
                    if len(sentence.strip()) > 20:
                        self.extract_pairs_from_text(sentence)
            
            print(f"  ✓ Completed")
        except Exception as e:
            print(f"  Error: {e}")
    
    def process_all_sources(self):
        print("=" * 60)
        print("EXPANDED SEMANTIC PAIR EXTRACTION - FIXED")
        print("=" * 60)
        print()
        
        # Process 20 newsgroups CSV (FIXED)
        newsgroups = self.data_dir / "20newsgroup_preprocessed.csv"
        if newsgroups.exists():
            self.process_csv(newsgroups)
        
        # Process text files
        text_files = [
            "art_of_war.txt",
            "frankenstein.txt",
            "all_corpus.txt",
            "dialogue_corpus.txt"
        ]
        
        for filename in text_files:
            filepath = self.data_dir / filename
            if filepath.exists() and filepath.stat().st_size > 0:
                self.process_txt(filepath)
    
    def save_pairs(self, min_frequency=10):  # INCREASED from 2 to 10
        print()
        print("=" * 60)
        print("SAVING SEMANTIC PAIRS")
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
        print("Top 20 pairs:")
        for pair, count in sorted_pairs[:20]:
            w1, w2 = pair.split(':')
            print(f"  {w1:15s} ↔ {w2:15s} ({count:,})")

if __name__ == "__main__":
    extractor = ExpandedSemanticExtractor()
    extractor.process_all_sources()
    extractor.save_pairs(min_frequency=10)  # Only pairs that appear 10+ times
    
    print()
    print("=" * 60)
    print("✓ EXTRACTION COMPLETE")
    print("=" * 60)
