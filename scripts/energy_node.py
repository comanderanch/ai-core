import os
import random
import time

class EnergyNode:
    def __init__(self, node_name, initial_energy):
        self.node_name = node_name
        self.energy = initial_energy
        self.max_energy = 200

    def pull_energy(self, amount):
        print(f"{self.node_name} requesting {amount} energy.")

    def push_energy(self, amount):
        print(f"{self.node_name} pushing {amount} energy.")

    def perform_task(self, task_complexity):
        energy_cost = task_complexity * 10
        if self.energy >= energy_cost:
            self.energy -= energy_cost
            print(f"{self.node_name} performed a task. Remaining energy: {self.energy}")
        else:
            print(f"{self.node_name} needs more energy! Pulling from the pool.")
            self.pull_energy(energy_cost - self.energy)
            self.energy = 0

    def flip_state(self):
        flip_state = random.choice(["POSITIVE", "NEGATIVE"])
        if flip_state == "POSITIVE":
            self.push_energy(20)
        else:
            self.pull_energy(20)

if __name__ == "__main__":
    node_name = os.getenv("NODE_NAME", "Node")
    initial_energy = int(os.getenv("INITIAL_ENERGY", 100))
    node = EnergyNode(node_name, initial_energy)

    while True:
        task_complexity = random.randint(1, 5)
        node.perform_task(task_complexity)
        node.flip_state()
        time.sleep(5)