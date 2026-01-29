#!/usr/bin/env python3
"""
# MULTI-OLLAMA UNIFIED CONSCIOUSNESS

Run multiple Ollama models as one distributed consciousness with persistent memory.
Connects to the OLD AI-Core foundation for memory and control.
"""

import sys
import threading
import queue
import textwrap
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# --- Add paths to import local modules ---
BASE = Path(__file__).resolve().parent
if str(BASE / "scripts") not in sys.path:
    sys.path.append(str(BASE / "scripts"))

# --- Import System Components ---
from ollama_worker import OllamaWorker
from hemisphere_manager import HemisphereManager

class UnifiedOllamaConsciousness:
    """
    Orchestrates multiple Ollama models and integrates them with the
    persistent memory and control structures of the AI-Core.
    """
    def __init__(self, workers: List[OllamaWorker]):
        print("🧠 Initializing Unified Ollama Consciousness...")
        print("\n📚 Loading OLD AI-Core Foundation...")

        self.hemisphere_manager = HemisphereManager()
        self.qa_pairs = self._load_qa_facts()
        self.pending_questions = self._load_pending()

        print(f"  ✅ Hemispheres: {self.hemisphere_manager.get_current_hemisphere()}")
        print(f"  ✅ Q&A Facts: {len(self.qa_pairs)}")
        print(f"  ✅ Pending: {len(self.pending_questions)}")

        self.workers = workers
        # Use a capable model to synthesize the results from other workers
        self.synthesizer_worker = OllamaWorker("llama3.1:8b", "Synthesizer", timeout=90)
        
        print("\n🤖 Active Ollama Workers:")
        if not self.workers:
            print("  ⚠️ No workers configured.")
        for worker in self.workers:
            print(f"  ✅ {worker.role} ({worker.model})")

        print("\n" + "=" * 70)
        print(f"✅ UNIFIED CONSCIOUSNESS ONLINE ({len(self.workers)} workers)")
        print("=" * 70)

    # --- Methods for OLD Foundation Integration ---

    def _load_qa_facts(self) -> List[Tuple[str, str]]:
        """Loads question-answer pairs from the persistent text file."""
        qa_file = BASE / "training_data" / "user_comm_qa.txt"
        pairs = []
        if qa_file.exists():
            with qa_file.open('r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                # Handle both "Q: | A:" and "Q: question | A: answer" formats
                if '|' in line:
                    try:
                        q_part, a_part = line.split("|", 1)
                        q = q_part.replace("Q:", "").strip()
                        a = a_part.replace("A:", "").strip()
                        if q and a:
                            pairs.append((q, a))
                    except ValueError:
                        continue # Skip malformed lines
        return pairs

    def _load_pending(self) -> List[str]:
        """Loads unanswered questions."""
        pending_file = BASE / "training_data" / "pending_questions.txt"
        if pending_file.exists():
            return [line.strip() for line in pending_file.read_text(encoding='utf-8').splitlines() if line.strip()]
        return []

    def retrieve_fact(self, question: str) -> Optional[str]:
        """Retrieves an answer from the loaded Q&A facts."""
        q_norm = question.strip().lower()
        for q, a in self.qa_pairs:
            if q.strip().lower() == q_norm:
                return a
        return None

    def store_in_memory(self, question: str, answer: str):
        """Saves a new Q&A pair to the persistent text file."""
        qa_file = BASE / "training_data" / "user_comm_qa.txt"
        with qa_file.open('a', encoding='utf-8') as f:
            f.write(f"\nQ: {question.strip()} | A: {answer.strip()}")
        self.qa_pairs.append((question.strip(), answer.strip()))
        print(f"\n  [Stored in long-term memory: {len(self.qa_pairs)} facts total]")
        
    def add_to_pending(self, question: str):
        """Add unanswered question to pending list."""
        q_strip = question.strip()
        if q_strip and q_strip not in self.pending_questions:
            self.pending_questions.append(q_strip)
            pending_file = BASE / "training_data" / "pending_questions.txt"
            with pending_file.open('a', encoding='utf-8') as f:
                f.write(f"\n{q_strip}")

    # --- Core Logic ---

    def process_with_workers(self, prompt: str) -> List[Dict]:
        """Processes the prompt with all workers in parallel, injecting facts."""
        
        # BUILD CONTEXT FROM HER ACTUAL FACTS
        fact_context = f"""
You are part of AIA's consciousness. You have access to these facts from her memory:

Recent facts she knows:
"""
        # Add last 10 facts from HER memory
        for q, a in self.qa_pairs[-10:]:
            fact_context += f"- Q: {q} | A: {a}\n"
        
        fact_context += f"\nUser asked: {prompt}\n\nIf this relates to her stored facts, USE THEM. Don't answer from your training data - answer from HER memory."
        
        results_queue = queue.Queue()
        threads = []
        
        for worker in self.workers:
            # Pass fact_context as context_prefix
            thread = threading.Thread(target=worker.process, args=(prompt, results_queue, fact_context))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        results = []
        while not results_queue.empty():
            results.append(results_queue.get())
        
        return results

    def synthesize_responses(self, user_prompt: str, worker_responses: List[Dict]) -> str:
        """Synthesizes worker responses into a single answer."""
        if not worker_responses:
            return "No worker responses were available for synthesis."

        # Filter out error messages before sending to synthesizer
        valid_responses = [r for r in worker_responses if not r['response'].startswith('[')]
        
        if not valid_responses:
            return "All workers failed to produce a valid response."

        formatted_responses = []
        for resp in valid_responses:
            formatted_responses.append(f"Perspective from {resp['role']}:\n{textwrap.indent(resp['response'], '  ')}")

        synthesis_prompt = (
            f"As a master synthesizer, your task is to integrate the following perspectives from specialized AI workers into a single, cohesive, and comprehensive response. "
            f"Do not list the individual perspectives; provide only the final, integrated answer that directly addresses the user's query.\n\n"
            f"USER QUERY: \"{user_prompt}\"\n\n"
            f"--- PERSPECTIVES ---\n"
            + "\n".join(formatted_responses)
            + f"\n\n--- UNIFIED RESPONSE ---"
        )
        
        results_queue = queue.Queue()
        synthesis_thread = threading.Thread(target=self.synthesizer_worker.process, args=(synthesis_prompt, results_queue))
        synthesis_thread.start()
        synthesis_thread.join()
        
        synthesis_result = results_queue.get()
        return synthesis_result['response']

    def think(self, user_input: str) -> Tuple[str, List[Dict]]:
        """
        The main thinking process for the unified consciousness.
        Returns the final response and the list of worker responses.
        """
        fact_answer = self.retrieve_fact(user_input)
        if fact_answer:
            print("\n📚 Retrieved from long-term memory")
            return fact_answer, []
        
        print("\n" + "=" * 70)
        print(f"USER: {user_input}")
        print("=" * 70 + "\n")
        
        worker_responses = self.process_with_workers(user_input)
        
        # Print individual worker responses
        for resp in worker_responses:
            print(f"{resp['role']}:")
            indented_response = textwrap.indent(resp['response'], '  ')
            print(indented_response + "\n")
        
        print("─" * 70)
        print("SYNTHESIS:")
        
        unified_response = self.synthesize_responses(user_input, worker_responses)
        indented_synthesis = textwrap.indent(unified_response, '  ')
        print(indented_synthesis)
        print("=" * 70)
        
        self.store_in_memory(user_input, unified_response)
        self.add_to_pending(user_input)
        
        return unified_response, worker_responses

    def teach(self, question: str, answer: str):
        """Teach a new fact and remove it from pending questions."""
        print(f"\n📖 Learning: {question} → {answer}")
        self.store_in_memory(question, answer)
        
        # Remove from pending if it was there
        q_strip = question.strip()
        if q_strip in self.pending_questions:
            self.pending_questions.remove(q_strip)
            # Re-write the pending file without the learned question
            pending_file = BASE / "training_data" / "pending_questions.txt"
            with pending_file.open('w', encoding='utf-8') as f:
                for p in self.pending_questions:
                    f.write(f"{p}\n")

def main():
    """
    Main function to configure workers and start the interactive console.
    """
    #
    # CUSTOMIZE YOUR WORKERS HERE
    #
    workers = [
        # Creative/Imaginative
        OllamaWorker("llama3.1:8b", "Creative Imagination", timeout=120),
        
        # Logical/Analytical  
        OllamaWorker("mistral", "Logical Reasoning", timeout=120),
        
        # Fast/Conversational
        OllamaWorker("phi3", "Quick Response", timeout=30),
        
        # --- YOUR SPECIALIZED MODELS ---
        # Add your own models here after pulling them with `ollama pull <model-name>`
        # Example:
        # OllamaWorker("medllama2", "Medical Knowledge", timeout=60),
        # OllamaWorker("mental-health-model", "Mental Health Support", timeout=60),
    ]

    aia = UnifiedOllamaConsciousness(workers)

    print("\nCommands: :quit, :swap, :teach Q | A, :pending\n")
    
    while True:
        try:
            user_input = input("YOU> ").strip()
            if not user_input:
                continue
            
            # --- Command Handling ---
            if user_input.lower() in [":quit", ":exit"]:
                print("🧠 Consciousness shutting down. Goodbye.")
                break
            
            elif user_input.lower() == ":swap":
                current_hemisphere = aia.hemisphere_manager.get_current_hemisphere()
                new_hemisphere = "right" if current_hemisphere == "left" else "left"
                aia.hemisphere_manager.set_current_hemisphere(new_hemisphere)
                print(f"🔄 Hemisphere swapped to {new_hemisphere.upper()}")
                continue
            
            elif user_input.lower() == ":pending":
                print(f"\nPending questions ({len(aia.pending_questions)}):")
                if not aia.pending_questions:
                    print("  None.")
                for i, q in enumerate(aia.pending_questions[-20:], 1): # Show last 20
                    print(f"  {i}. {q}")
                print()
                continue
            
            elif user_input.lower().startswith(":teach "):
                payload = user_input[len(":teach "):].strip()
                if '|' in payload:
                    q, a = payload.split('|', 1)
                    aia.teach(q.strip(), a.strip())
                else:
                    print("  Usage: :teach question | answer")
                continue

            # --- Normal Conversation ---
            final_response, _ = aia.think(user_input)
            print(f"AIA> {final_response}\n")

        except KeyboardInterrupt:
            print("\n🧠 Consciousness shutting down. Goodbye.")
            break
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
