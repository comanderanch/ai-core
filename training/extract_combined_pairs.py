#!/usr/bin/env python3
"""
AI-Core Standalone: Combined Semantic Pair Extraction
======================================================

Extracts semantic pairs from BOTH sources:
1. 236 book chunk JSONL files (by_book/)
2. scraped_qa.jsonl (6,875 additional pairs)

Combined output: ~10,000+ diverse semantic training pairs

Author: comanderanch
Phase: 5.7 Standalone Resurrection - Diversity Boost
"""

import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Set
import re


class CombinedSemanticExtractor:
    """
    Extract semantic pairs from multiple data sources.
    
    Sources:
      1. Book chunks: /training_data/by_book/*.jsonl
      2. Scraped Q&A: scraped_qa.jsonl
    
    Combines all sources into unified semantic pair dataset.
    """
    
    def __init__(
        self,
        book_chunks_dir: str = "/home/comanderanch/ai-core/training_data/by_book",
        scraped_qa_file: str = "/home/comanderanch/ai-core/training_data/scraped_qa.jsonl",
        output_file: str = "training/combined_semantic_pairs.txt",
        min_pair_frequency: int = 2
    ):
        """Initialize combined extractor."""
        self.book_chunks_dir = Path(book_chunks_dir)
        self.scraped_qa_file = Path(scraped_qa_file)
        self.output_file = Path(output_file)
        self.min_pair_frequency = min_pair_frequency
        
        # Word associations
        self.word_pairs = defaultdict(int)
        self.word_contexts = defaultdict(list)
        
        # Color heuristics
        self.color_ranges = self._init_color_ranges()
        
        # Statistics
        self.stats = {
            'book_chunks_qa': 0,
            'scraped_qa': 0,
            'total_qa': 0,
            'unique_words': set(),
            'total_pairs': 0
        }
        
        print(f"[✓] Combined Semantic Extractor initialized")
        print(f"    Book chunks: {self.book_chunks_dir}")
        print(f"    Scraped Q&A: {self.scraped_qa_file}")
        print(f"    Output: {self.output_file}")
    
    def _init_color_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Color psychology mappings (same as before)."""
        return {
            # Red family (0-200): Energy, danger, passion, hot
            'fire': (0, 50), 'hot': (0, 50), 'heat': (0, 50),
            'danger': (0, 50), 'warning': (0, 50), 'alert': (0, 50),
            'anger': (0, 50), 'rage': (0, 50), 'fury': (0, 50),
            'passion': (10, 60), 'love': (10, 60), 'desire': (10, 60),
            'blood': (0, 50), 'red': (0, 50), 'stop': (0, 30),
            'fast': (0, 50), 'quick': (0, 50), 'rapid': (0, 50),
            
            # Orange family (200-400)
            'warm': (200, 300), 'creative': (200, 300),
            'autumn': (200, 300), 'sunset': (200, 300),
            'caution': (250, 350), 'orange': (200, 300),
            
            # Yellow family (400-600)
            'bright': (400, 500), 'light': (400, 500),
            'happy': (400, 500), 'joy': (400, 500),
            'sun': (400, 500), 'gold': (450, 550),
            'attention': (400, 500), 'energy': (400, 500),
            
            # Green family (600-1000)
            'nature': (600, 800), 'growth': (600, 800),
            'tree': (600, 800), 'grass': (600, 800), 'forest': (600, 800),
            'balance': (650, 850), 'health': (650, 850),
            'safe': (700, 800), 'go': (700, 800), 'start': (700, 800),
            'green': (600, 800), 'life': (600, 800),
            
            # Blue family (1000-1400)
            'cool': (1000, 1200), 'cold': (1000, 1200),
            'calm': (1000, 1200), 'peace': (1000, 1200),
            'sky': (1000, 1200), 'ocean': (1050, 1250),
            'water': (1050, 1250), 'blue': (1000, 1200),
            'sad': (1000, 1200), 'depth': (1100, 1300),
            'trust': (1050, 1250), 'slow': (1000, 1200),
            
            # Purple family (1400-1800)
            'mystery': (1400, 1600), 'wisdom': (1400, 1600),
            'magic': (1400, 1600), 'royal': (1400, 1600),
            'luxury': (1450, 1650), 'purple': (1400, 1600),
            'spirit': (1400, 1600), 'dream': (1400, 1600),
            
            # Grayscale (1800-2303)
            'neutral': (1800, 2000), 'balance': (1850, 2050),
            'clarity': (1900, 2100), 'empty': (1800, 1900),
            'full': (2100, 2300), 'black': (1800, 1850),
            'white': (2250, 2303), 'gray': (1950, 2050),
            
            # Abstract concepts
            'question': (400, 600), 'answer': (600, 800),
            'problem': (0, 200), 'solution': (600, 800),
            'input': (1000, 1200), 'output': (600, 800),
            'start': (400, 600), 'end': (0, 200),
            'true': (600, 800), 'false': (0, 200),
            'yes': (600, 800), 'no': (0, 200),
            'good': (600, 800), 'bad': (0, 200),
            'right': (600, 800), 'wrong': (0, 200),
            'up': (400, 600), 'down': (0, 200),
            'high': (400, 600), 'low': (0, 200),
            'big': (400, 600), 'small': (1800, 2000),
            'more': (600, 800), 'less': (1800, 2000),
            
            # Logic/Boolean (from scraped_qa)
            'closed': (0, 200), 'open': (600, 800),
            'pressed': (0, 200), 'released': (600, 800),
            'on': (400, 600), 'off': (1800, 2000),
            'logic': (1000, 1200), 'circuit': (1000, 1200),
            'switch': (400, 600), 'lamp': (400, 600),
            'complement': (1400, 1600), 'variable': (1000, 1200),
            'operation': (1000, 1200), 'expression': (1000, 1200),
            
            # Mathematics
            'domain': (600, 800), 'range': (600, 800),
            'function': (1000, 1200), 'equation': (1000, 1200),
            'horizontal': (1000, 1200), 'vertical': (400, 600),
        }
    
    def extract_words(self, text: str) -> List[str]:
        """Extract meaningful words from text."""
        text = text.lower()
        words = re.findall(r'\b[a-z]{3,}\b', text)
        
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all',
            'can', 'her', 'was', 'one', 'our', 'out', 'day', 'get',
            'has', 'him', 'his', 'how', 'its', 'may', 'now', 'old',
            'see', 'than', 'that', 'this', 'what', 'when', 'where',
            'who', 'will', 'with', 'from', 'have', 'been',
            'were', 'said', 'each', 'which', 'their', 'time',
            'way', 'about', 'many', 'then', 'them', 'would', 'like',
            'into', 'than', 'other', 'some', 'could', 'these',
        }
        
        words = [w for w in words if w not in stop_words and len(w) >= 3]
        return words
    
    def process_qa_pair(self, question: str, answer: str, source: str):
        """
        Process single Q&A pair.
        
        Args:
            question: Question text
            answer: Answer text
            source: Data source identifier
        """
        if not question or not answer:
            return
        
        self.stats['total_qa'] += 1
        
        # Extract words
        q_words = self.extract_words(question)
        a_words = self.extract_words(answer)
        
        # Build associations
        for q_word in q_words:
            self.stats['unique_words'].add(q_word)
            for a_word in a_words:
                self.stats['unique_words'].add(a_word)
                
                # Store pair
                pair = tuple(sorted([q_word, a_word]))
                self.word_pairs[pair] += 1
        
        # Store context
        context = question + " " + answer
        for word in set(q_words + a_words):
            self.word_contexts[word].append(context[:100])
    
    def process_book_chunks(self):
        """Process all book chunk JSONL files."""
        print(f"\n[*] Processing book chunks from: {self.book_chunks_dir}")
        
        jsonl_files = list(self.book_chunks_dir.glob("*.jsonl"))
        total_books = len(jsonl_files)
        
        print(f"[*] Found {total_books} book chunk files")
        
        for idx, filepath in enumerate(jsonl_files, 1):
            if idx % 50 == 0:
                print(f"    Progress: {idx}/{total_books} files...")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            data = json.loads(line.strip())
                            
                            # Skip meta events
                            if 'meta_event' in data:
                                continue
                            
                            question = data.get('question', '')
                            answer = data.get('answer', '')
                            
                            self.process_qa_pair(question, answer, 'book_chunk')
                            self.stats['book_chunks_qa'] += 1
                            
                        except json.JSONDecodeError:
                            continue
            
            except Exception as e:
                print(f"[!] Error processing {filepath.name}: {e}")
        
        print(f"[✓] Processed {total_books} book chunk files")
        print(f"[✓] Extracted {self.stats['book_chunks_qa']} Q&A pairs from book chunks")
    
    def process_scraped_qa(self):
        """Process scraped_qa.jsonl file."""
        print(f"\n[*] Processing scraped Q&A from: {self.scraped_qa_file}")
        
        if not self.scraped_qa_file.exists():
            print(f"[!] Warning: scraped_qa.jsonl not found at {self.scraped_qa_file}")
            return
        
        try:
            with open(self.scraped_qa_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        
                        question = data.get('question', '')
                        answer = data.get('answer', '')
                        
                        self.process_qa_pair(question, answer, 'scraped')
                        self.stats['scraped_qa'] += 1
                        
                    except json.JSONDecodeError:
                        continue
        
        except Exception as e:
            print(f"[!] Error processing scraped_qa.jsonl: {e}")
        
        print(f"[✓] Extracted {self.stats['scraped_qa']} Q&A pairs from scraped data")
    
    def map_word_to_tokens(self, word: str) -> List[int]:
        """Map word to color token range."""
        if word in self.color_ranges:
            start, end = self.color_ranges[word]
            step = (end - start) // 3
            return [start, start + step, start + 2*step]
        else:
            # Hash-based mapping
            hash_val = hash(word) % 2304
            return [hash_val, (hash_val + 768) % 2304, (hash_val + 1536) % 2304]
    
    def generate_training_pairs(self) -> List[Tuple[str, str, List[int], List[int]]]:
        """Generate training pairs from word associations."""
        training_pairs = []
        
        for (word1, word2), count in self.word_pairs.items():
            if count >= self.min_pair_frequency:
                tokens1 = self.map_word_to_tokens(word1)
                tokens2 = self.map_word_to_tokens(word2)
                training_pairs.append((word1, word2, tokens1, tokens2))
        
        return training_pairs
    
    def save_training_pairs(self, pairs: List[Tuple[str, str, List[int], List[int]]]):
        """Save training pairs to file."""
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.output_file, 'w') as f:
            # Write header
            f.write("# AI-Core Combined Semantic Training Pairs\n")
            f.write("# Sources: book chunks + scraped_qa.jsonl\n")
            f.write(f"# Total pairs: {len(pairs)}\n")
            f.write("#\n")
            
            for word1, word2, tokens1, tokens2 in pairs:
                tokens1_str = ','.join(map(str, tokens1))
                tokens2_str = ','.join(map(str, tokens2))
                f.write(f"{word1} {word2} {tokens1_str} {tokens2_str}\n")
        
        print(f"\n[✓] Saved {len(pairs)} training pairs to: {self.output_file}")
    
    def run(self):
        """Run complete extraction pipeline."""
        print("="*60)
        print("COMBINED SEMANTIC PAIR EXTRACTION")
        print("="*60)
        
        # Process both sources
        self.process_book_chunks()
        self.process_scraped_qa()
        
        # Generate training pairs
        print(f"\n[*] Generating training pairs (min frequency: {self.min_pair_frequency})...")
        pairs = self.generate_training_pairs()
        
        # Save
        self.save_training_pairs(pairs)
        
        # Statistics
        print("\n" + "="*60)
        print("EXTRACTION COMPLETE - COMBINED DATASET")
        print("="*60)
        print(f"Source breakdown:")
        print(f"  Book chunks: {self.stats['book_chunks_qa']} Q&A pairs")
        print(f"  Scraped Q&A: {self.stats['scraped_qa']} Q&A pairs")
        print(f"  TOTAL Q&A: {self.stats['total_qa']} pairs")
        print(f"")
        print(f"Semantic extraction:")
        print(f"  Unique words: {len(self.stats['unique_words'])}")
        print(f"  Word pair associations: {len(self.word_pairs)}")
        print(f"  Training pairs (filtered): {len(pairs)}")
        print(f"")
        print(f"Output: {self.output_file}")
        print("="*60)


if __name__ == "__main__":
    extractor = CombinedSemanticExtractor(
        book_chunks_dir="/home/comanderanch/ai-core/training_data/by_book",
        scraped_qa_file="/home/comanderanch/ai-core/training_data/scraped_qa.jsonl",
        output_file="training/combined_semantic_pairs.txt",
        min_pair_frequency=2
    )
    
    extractor.run()