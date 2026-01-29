import requests
import json
import time

class OllamaWorker:
    """
    A worker that communicates with a specific Ollama model.
    Designed to be run in a separate thread.
    """
    def __init__(self, model, role, timeout=60):
        """
        Initializes the OllamaWorker.

        Args:
            model (str): The name of the Ollama model to use (e.g., "llama3.1:8b").
            role (str): The specialized role of this worker (e.g., "Creative Imagination").
            timeout (int): The timeout in seconds for the API request.
        """
        self.model = model
        self.role = role
        self.timeout = timeout
        self.api_url = "http://localhost:11434/api/generate"

    def process(self, prompt, results_queue, context_prefix=""):
        """
        Processes a prompt with the assigned Ollama model and puts the result in a queue.

        Args:
            prompt (str): The user prompt to send to the model.
            results_queue (queue.Queue): The queue to store the output dictionary.
            context_prefix (str): Optional context to prepend to the prompt (e.g., facts).
        """
        full_prompt = context_prefix + prompt if context_prefix else prompt
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False  # We want the full response at once
        }
        
        response_text = ""
        try:
            start_time = time.time()
            response = requests.post(
                self.api_url, 
                json=payload, 
                timeout=self.timeout
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # The response from Ollama is a stream of JSON objects, one per line
            # We take the final one which contains the full response
            lines = response.text.strip().split('\n')
            final_line = json.loads(lines[-1])
            response_text = final_line.get("response", "").strip()
            end_time = time.time()
            # print(f"DEBUG: {self.role} responded in {end_time - start_time:.2f} seconds.") # Debug line

        except requests.exceptions.Timeout:
            response_text = f"[{self.role} timed out after {self.timeout} seconds]"
        except requests.exceptions.RequestException as e:
            response_text = f"[{self.role} API error: {e}]"
        except (json.JSONDecodeError, IndexError):
            response_text = f"[{self.role} could not parse response from Ollama]"
        except Exception as e:
            response_text = f"[{self.role} encountered an unexpected error: {e}]"

        results_queue.put({
            "role": self.role,
            "response": response_text
        })
