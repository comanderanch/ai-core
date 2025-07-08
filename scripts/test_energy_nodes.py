from energy_node import EnergyNode as Node1
from energy_node_2 import EnergyNode as Node2

# Initialize both nodes
node1 = Node1("Node1", initial_energy=120)
node2 = Node2("Node2", initial_energy=80)

print("\n[TEST] Initialized Node1 with 120 energy")
print("[TEST] Initialized Node2 with 80 energy")

# Simulate tasks and flips for both nodes
for cycle in range(3):
    print(f"\n--- Cycle {cycle + 1} ---")

    task1 = (cycle + 1)  # Gradually increasing complexity
    print(f"\n[Node1] Performing task with complexity {task1}")
    node1.perform_task(task1)
    node1.flip_state()

    task2 = (cycle + 2)  # Slightly higher complexity
    print(f"\n[Node2] Performing task with complexity {task2}")
    node2.perform_task(task2)
    node2.flip_state()

# Final state overview
print("\n[RESULT] Final Node States:")
print(f"Node1 Remaining Energy: {node1.energy}")
print(f"Node2 Remaining Energy: {node2.energy}")
