# behavior_trigger_system.py
import json
from datetime import datetime
import os

class BehaviorTriggerSystem:
    def __init__(self, decision_chain_manager):
        """
        Initialize the Behavior Trigger System
        :param decision_chain_manager: The Decision Chain Manager that handles events
        """
        self.decision_chain_manager = decision_chain_manager
        self.memory = {}  # A simple dictionary to simulate memory updates

    

    def execute_triggered_action(self, action):
        """
        Execute the action triggered by the decision chain and log reflex feedback.
        :param action: The action to execute (as a string)
        """
        print(f"Executing behavior for action: {action}")
        
        # Log reflex feedback to memory/reflex_feedback_log.json
        feedback_entry = {
            "action": action,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        log_path = os.path.join("memory", "reflex_feedback_log.json")
        existing = []

        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    print("[FeedbackLog] Warning: Existing log is invalid, starting fresh.")

        existing.append(feedback_entry)

        with open(log_path, "w") as f:
            json.dump(existing, f, indent=4)

        # Continue normal execution
        if action == "Trigger Action A":
            self.trigger_action_a()
        elif action == "Trigger Action B":
            self.trigger_action_b()
        else:
            print("Unknown action.")


    def trigger_action_a(self):
        """
        Action A could trigger a memory update or other system behaviors.
        In this case, we'll simulate updating the memory.
        """
        print("Triggering Action A: Updating memory for token ID 20.")
        self.memory["token_20"] = "Action A triggered"
        self.display_memory()

    def trigger_action_b(self):
        """
        Action B could also trigger memory updates or other behaviors.
        """
        print("Triggering Action B: Updating memory for token ID 40.")
        self.memory["token_40"] = "Action B triggered"
        self.display_memory()

    def display_memory(self):
        """
        Display the current memory state (for debugging purposes).
        """
        print("Current memory state:", self.memory)

# Example usage
if __name__ == "__main__":
    # Assume decision_chain_manager has been defined already
    from decision_chain_manager import DecisionChainManager, TokenMonitor

    token_monitor = TokenMonitor()
    decision_chain_manager = DecisionChainManager(token_monitor)
    
    behavior_trigger_system = BehaviorTriggerSystem(decision_chain_manager)
    
    # Simulate the decision process and trigger corresponding behaviors
    decision_chain_manager.listen_for_token_events()
    behavior_trigger_system.execute_triggered_action("Trigger Action A")
    behavior_trigger_system.execute_triggered_action("Trigger Action B")

# === External Reflex Trigger Entry Point ===

# === External Reflex Trigger Entry Point ===

def load_action_weights():
    path = "memory/reflex_behavior_summary.json"
    weights = {}
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                data = json.load(f)
                for entry in data:
                    weights[entry["action"]] = entry["count"]
            except json.JSONDecodeError:
                print("[Behavior] Warning: Summary file is invalid.")
    return weights


# Global instance (can be reused across modules)
behavior_trigger_system_instance = None

def trigger_from_tokens(tokens):
    global behavior_trigger_system_instance

    if behavior_trigger_system_instance is None:
        from decision_chain_manager import DecisionChainManager, TokenMonitor
        token_monitor = TokenMonitor()
        decision_chain_manager = DecisionChainManager(token_monitor)
        behavior_trigger_system_instance = BehaviorTriggerSystem(decision_chain_manager)

    action_weights = load_action_weights()

    for token in tokens:
        print(f"[External Trigger] Processing token: {token}")

        if token == 20:
            action = "Trigger Action A"
        elif token == 40:
            action = "Trigger Action B"
        else:
            print(f"No behavior mapped for token {token}")
            continue

        weight = action_weights.get(action, 0)
        print(f"[Weighted Reflex] Action: {action}, Weight: {weight}")

        if weight >= 1:
            behavior_trigger_system_instance.execute_triggered_action(action)
        else:
            print(f"[Reflex] Action {action} skipped due to low priority.")


