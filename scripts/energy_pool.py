import os

class EnergyPool:
    def __init__(self, battery_capacity):
        self.total_energy = 1000
        self.battery_capacity = battery_capacity
        self.battery_storage = 0

    def pull_energy(self, amount):
        if self.battery_storage > 0:
            if amount <= self.battery_storage:
                self.battery_storage -= amount
                print(f"Pulled {amount} from the battery. Battery storage: {self.battery_storage}")
                return
            else:
                amount -= self.battery_storage
                print(f"Pulled {self.battery_storage} from the battery. Now pulling {amount} from the pool.")
                self.battery_storage = 0

        if amount <= self.total_energy:
            self.total_energy -= amount
            print(f"Pulled {amount} energy from the pool. Remaining pool energy: {self.total_energy}")
        else:
            print(f"Not enough energy in the pool! Requested: {amount}, Available: {self.total_energy}")

    def push_energy(self, amount):
        if self.battery_storage + amount <= self.battery_capacity:
            self.battery_storage += amount
            print(f"Pushed {amount} energy into the battery. Battery storage: {self.battery_storage}")
        else:
            surplus = amount - (self.battery_capacity - self.battery_storage)
            self.battery_storage = self.battery_capacity
            self.total_energy += surplus
            print(f"Battery full! Pushed {surplus} energy into the pool. Pool energy: {self.total_energy}")

if __name__ == "__main__":
    battery_capacity = int(os.getenv("BATTERY_CAPACITY", 500))
    energy_pool = EnergyPool(battery_capacity)
    energy_pool.push_energy(200)
    energy_pool.pull_energy(150)