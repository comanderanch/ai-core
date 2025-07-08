# test_energy_pool.py

from energy_pool import EnergyPool

def test_energy_pool():
    print("[Test] Initializing EnergyPool with battery capacity = 500")
    pool = EnergyPool(battery_capacity=500)

    print("\n[Test] Pushing 300 energy into battery...")
    pool.push_energy(300)

    print("\n[Test] Pulling 200 energy...")
    pool.pull_energy(200)

    print("\n[Test] Pulling 400 energy (should deplete battery and use pool)...")
    pool.pull_energy(400)

    print("\n[Test] Pushing 600 energy (should overflow into pool)...")
    pool.push_energy(600)

    print("\n[Result] Final Energy States:")
    print(f"  Battery Storage: {pool.battery_storage}")
    print(f"  Pool Energy: {pool.total_energy}")

if __name__ == "__main__":
    test_energy_pool()
