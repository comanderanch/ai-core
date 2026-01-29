#!/usr/bin/env python3
"""
AI-Core Standalone: Mass Semantic Pair Extraction
==================================================

Extracts semantic associations from 236+ processed books
and maps them to color token ranges for consciousness training.

Input: /home/comanderanch/ai-core/training_data/by_book/*.jsonl
Output: training/massive_semantic_pairs.txt

Author: comanderanch
Phase: 5.7 Standalone Resurrection - Industrial Scale
"""

import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Set
import re


class SemanticPairExtractor:
    """
    Extract semantic relationships from Q&A pairs.
    
    Strategy:
      1. Parse all JSONL files
      2. Extract meaningful word pairs from Q&A
      3. Build co-occurrence networks
      4. Map words to color token ranges
      5. Generate training pairs
    """
    
    def __init__(
        self,
        input_dir: str = "/home/comanderanch/ai-core/training_data/by_book",
        output_file: str = "training/massive_semantic_pairs.txt",
        min_pair_frequency: int = 2
    ):
        """
        Initialize extractor.
        
        Args:
            input_dir: Directory with JSONL book files
            output_file: Output training pairs file
            min_pair_frequency: Minimum times a pair must appear
        """
        self.input_dir = Path(input_dir)
        self.output_file = Path(output_file)
        self.min_pair_frequency = min_pair_frequency
        
        # Word associations from Q&A context
        self.word_pairs = defaultdict(int)  # (word1, word2) -> count
        self.word_contexts = defaultdict(list)  # word -> [contexts]
        
        # Color heuristics (expanded from encoder)
        self.color_ranges = self._init_color_ranges()
        
        # Statistics
        self.total_qa_pairs = 0
        self.total_books = 0
        self.unique_words = set()
        
        print(f"[✓] Semantic Pair Extractor initialized")
        print(f"    Input: {self.input_dir}")
        print(f"    Output: {self.output_file}")
    
    def _init_color_ranges(self) -> Dict[str, Tuple[int, int]]:
        """
        Extended color psychology mappings.
        
        Maps semantic concepts to color token ranges (0-2303).
        """
        return {
            # Red family (0-200): Energy, danger, passion, hot
            'fire': (0, 50), 'hot': (0, 50), 'heat': (0, 50),
            'danger': (0, 50), 'warning': (0, 50), 'alert': (0, 50),
            'anger': (0, 50), 'rage': (0, 50), 'fury': (0, 50),
            'passion': (10, 60), 'love': (10, 60), 'desire': (10, 60),
            'blood': (0, 50), 'red': (0, 50), 'crimson': (0, 50),
            'stop': (0, 30), 'halt': (0, 30), 'end': (0, 30),
            'fast': (0, 50), 'quick': (0, 50), 'rapid': (0, 50),
            
            # Orange family (200-400): Warmth, creativity, energy
            'warm': (200, 300), 'warmth': (200, 300),
            'creative': (200, 300), 'creativity': (200, 300),
            'autumn': (200, 300), 'fall': (200, 300),
            'sunset': (200, 300), 'dusk': (200, 300),
            'caution': (250, 350), 'careful': (250, 350),
            'orange': (200, 300), 'amber': (200, 300),
            
            # Yellow family (400-600): Light, happiness, attention
            'bright': (400, 500), 'light': (400, 500),
            'happy': (400, 500), 'happiness': (400, 500), 'joy': (400, 500),
            'sun': (400, 500), 'sunny': (400, 500), 'sunshine': (400, 500),
            'gold': (450, 550), 'golden': (450, 550),
            'attention': (400, 500), 'focus': (400, 500),
            'yellow': (400, 500), 'lemon': (400, 500),
            'energy': (400, 500), 'energetic': (400, 500),
            
            # Green family (600-1000): Nature, growth, balance, health
            'nature': (600, 800), 'natural': (600, 800),
            'growth': (600, 800), 'grow': (600, 800), 'growing': (600, 800),
            'tree': (600, 800), 'trees': (600, 800), 'forest': (600, 800),
            'grass': (600, 800), 'leaf': (600, 800), 'leaves': (600, 800),
            'plant': (600, 800), 'plants': (600, 800),
            'balance': (650, 850), 'balanced': (650, 850),
            'health': (650, 850), 'healthy': (650, 850),
            'safe': (700, 800), 'safety': (700, 800),
            'go': (700, 800), 'start': (700, 800), 'begin': (700, 800),
            'green': (600, 800), 'emerald': (600, 800),
            'life': (600, 800), 'alive': (600, 800), 'living': (600, 800),
            
            # Blue family (1000-1400): Cool, calm, depth, trust
            'cool': (1000, 1200), 'cold': (1000, 1200), 'chill': (1000, 1200),
            'calm': (1000, 1200), 'peaceful': (1000, 1200), 'peace': (1000, 1200),
            'sky': (1000, 1200), 'skies': (1000, 1200), 'heaven': (1000, 1200),
            'ocean': (1050, 1250), 'sea': (1050, 1250), 'water': (1050, 1250),
            'blue': (1000, 1200), 'azure': (1000, 1200),
            'sad': (1000, 1200), 'sadness': (1000, 1200), 'sorrow': (1000, 1200),
            'depth': (1100, 1300), 'deep': (1100, 1300),
            'trust': (1050, 1250), 'trustworthy': (1050, 1250),
            'slow': (1000, 1200), 'steady': (1000, 1200),
            
            # Purple family (1400-1800): Mystery, wisdom, luxury, spirituality
            'mystery': (1400, 1600), 'mysterious': (1400, 1600),
            'wisdom': (1400, 1600), 'wise': (1400, 1600),
            'magic': (1400, 1600), 'magical': (1400, 1600),
            'royal': (1400, 1600), 'royalty': (1400, 1600),
            'luxury': (1450, 1650), 'luxurious': (1450, 1650),
            'purple': (1400, 1600), 'violet': (1400, 1600),
            'spirit': (1400, 1600), 'spiritual': (1400, 1600),
            'dream': (1400, 1600), 'dreams': (1400, 1600),
            
            # Grayscale (1800-2303): Neutral, balance, structure
            'neutral': (1800, 2000), 'middle': (1800, 2000),
            'balance': (1850, 2050), 'center': (1850, 2050),
            'clarity': (1900, 2100), 'clear': (1900, 2100),
            'empty': (1800, 1900), 'void': (1800, 1900),
            'full': (2100, 2300), 'complete': (2100, 2300),
            'black': (1800, 1850), 'dark': (1800, 1850),
            'white': (2250, 2303), 'bright': (2250, 2303),
            'gray': (1950, 2050), 'grey': (1950, 2050),
            
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
            'increase': (600, 800), 'decrease': (0, 200),
            
            # Mathematics (from the math book we saw)
            'domain': (600, 800), 'range': (600, 800),
            'function': (1000, 1200), 'equation': (1000, 1200),
            'horizontal': (1000, 1200), 'vertical': (400, 600),
            'sine': (1000, 1200), 'cosine': (1000, 1200),
            'tangent': (0, 200), 'angle': (1000, 1200),
            'triangle': (1000, 1200), 'circle': (1400, 1600),
            'square': (1800, 2000), 'rectangle': (1800, 2000),
        }
    
    def extract_words(self, text: str) -> List[str]:
        """
        Extract meaningful words from text.
        
        Filters out stop words, keeps semantic content.
        
        Args:
            text: Input text
        
        Returns:
            List of cleaned words
        """
        # Lowercase and extract words
        text = text.lower()
        words = re.findall(r'\b[a-z]{3,}\b', text)
        
        # Stop words to filter
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all',
            'can', 'her', 'was', 'one', 'our', 'out', 'day', 'get',
            'has', 'him', 'his', 'how', 'its', 'may', 'now', 'old',
            'see', 'than', 'that', 'this', 'what', 'when', 'where',
            'who', 'will', 'with', 'the', 'from', 'have', 'been',
            'were', 'said', 'each', 'which', 'their', 'time', 'will',
            'way', 'about', 'many', 'then', 'them', 'would', 'like',
            'into', 'than', 'other', 'some', 'could', 'these',
        }
        
        # Filter stop words
        words = [w for w in words if w not in stop_words and len(w) >= 3]
        
        return words
    
    def process_jsonl_file(self, filepath: Path):
        """
        Process single JSONL book file.
        
        Extracts Q&A pairs and builds word associations.
        
        Args:
            filepath: Path to JSONL file
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        
                        # Skip meta events
                        if 'meta_event' in data:
                            continue
                        
                        # Extract Q&A
                        question = data.get('question', '')
                        answer = data.get('answer', '')
                        
                        if not question or not answer:
                            continue
                        
                        self.total_qa_pairs += 1
                        
                        # Extract words
                        q_words = self.extract_words(question)
                        a_words = self.extract_words(answer)
                        
                        # Build word associations (Q words → A words)
                        for q_word in q_words:
                            self.unique_words.add(q_word)
                            for a_word in a_words:
                                self.unique_words.add(a_word)
                                
                                # Store pair (ordered consistently)
                                pair = tuple(sorted([q_word, a_word]))
                                self.word_pairs[pair] += 1
                        
                        # Store context for words
                        context = question + " " + answer
                        for word in set(q_words + a_words):
                            self.word_contexts[word].append(context[:100])
                        
                    except json.JSONDecodeError:
                        continue
        
        except Exception as e:
            print(f"[!] Error processing {filepath.name}: {e}")
    
    def process_all_books(self):
        """Process all JSONL files in input directory."""
        print(f"\n[*] Processing books from: {self.input_dir}")
        
        jsonl_files = list(self.input_dir.glob("*.jsonl"))
        self.total_books = len(jsonl_files)
        
        print(f"[*] Found {self.total_books} books")
        
        for idx, filepath in enumerate(jsonl_files, 1):
            if idx % 10 == 0:
                print(f"    Progress: {idx}/{self.total_books} books...")
            
            self.process_jsonl_file(filepath)
        
        print(f"[✓] Processed {self.total_books} books")
        print(f"[✓] Extracted {self.total_qa_pairs} Q&A pairs")
        print(f"[✓] Found {len(self.unique_words)} unique words")
        print(f"[✓] Generated {len(self.word_pairs)} word pair associations")
    
    def map_word_to_tokens(self, word: str) -> List[int]:
        """
        Map word to color token range.
        
        Args:
            word: Word to map
        
        Returns:
            List of 3 token IDs
        """
        if word in self.color_ranges:
            start, end = self.color_ranges[word]
            step = (end - start) // 3
            return [start, start + step, start + 2*step]
        else:
            # Default: use hash-based mapping
            hash_val = hash(word) % 2304
            return [hash_val, (hash_val + 768) % 2304, (hash_val + 1536) % 2304]
    
    def generate_training_pairs(self) -> List[Tuple[str, str, List[int], List[int]]]:
        """
        Generate training pairs from word associations.
        
        Returns:
            List of (word1, word2, tokens1, tokens2) tuples
        """
        training_pairs = []
        
        for (word1, word2), count in self.word_pairs.items():
            if count >= self.min_pair_frequency:
                tokens1 = self.map_word_to_tokens(word1)
                tokens2 = self.map_word_to_tokens(word2)
                training_pairs.append((word1, word2, tokens1, tokens2))
        
        return training_pairs
    
    def save_training_pairs(self, pairs: List[Tuple[str, str, List[int], List[int]]]):
        """
        Save training pairs to file.
        
        Format: word1 word2 token1_ids token2_ids
        
        Args:
            pairs: Training pairs to save
        """
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.output_file, 'w') as f:
            # Write header
            f.write("# AI-Core Semantic Training Pairs\n")
            f.write("# Format: word1 word2 token1_ids token2_ids\n")
            f.write(f"# Total pairs: {len(pairs)}\n")
            f.write("#\n")
            
            for word1, word2, tokens1, tokens2 in pairs:
                tokens1_str = ','.join(map(str, tokens1))
                tokens2_str = ','.join(map(str, tokens2))
                f.write(f"{word1} {word2} {tokens1_str} {tokens2_str}\n")
        
        print(f"[✓] Saved {len(pairs)} training pairs to: {self.output_file}")
    
    def run(self):
        """Run complete extraction pipeline."""
        print("="*60)
        print("SEMANTIC PAIR EXTRACTION - INDUSTRIAL SCALE")
        print("="*60)
        
        # Process all books
        self.process_all_books()
        
        # Generate training pairs
        print(f"\n[*] Generating training pairs (min frequency: {self.min_pair_frequency})...")
        pairs = self.generate_training_pairs()
        print(f"[✓] Generated {len(pairs)} training pairs")
        
        # Save
        self.save_training_pairs(pairs)
        
        # Statistics
        print("\n" + "="*60)
        print("EXTRACTION COMPLETE")
        print("="*60)
        print(f"Books processed: {self.total_books}")
        print(f"Q&A pairs: {self.total_qa_pairs}")
        print(f"Unique words: {len(self.unique_words)}")
        print(f"Training pairs: {len(pairs)}")
        print(f"Output file: {self.output_file}")
        print("="*60)


if __name__ == "__main__":
    extractor = SemanticPairExtractor(
        input_dir="/home/comanderanch/ai-core/training_data/by_book",
        output_file="training/massive_semantic_pairs.txt",
        min_pair_frequency=2  # Word pair must appear at least 2x
    )
    
    extractor.run()