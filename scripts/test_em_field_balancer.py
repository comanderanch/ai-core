# test_em_field_balancer.py

from em_field_balancer import ElectromagneticField

# Initialize field with 1000 units
field = ElectromagneticField(field_strength=1000)

# Step 1: Detect fluctuations
fluctuation = field.detect_fluctuations()
print(f"[Step 1] Internal Fluctuation: {fluctuation:.2f}")

# Step 2: Detect resistance
resistance = field.detect_resistance()
print(f"[Step 2] External Resistance: {resistance:.2f}")

# Step 3: Balance field
kinetic = field.balance_field()
if kinetic > 0:
    print(f"[Step 3] Applied {kinetic:.2f} units of kinetic energy to stabilize.")
else:
    print("[Step 3] No balancing required.")

# Step 4: Apply force
force = field.apply_force()
if force:
    print(f"[Step 4] Applied {force:.2f} units of field force.")
else:
    print(f"[Step 4] Not enough field strength to apply force.")

# Final report
report = field.report()
print("\n[Final State]")
for k, v in report.items():
    print(f"{k}: {v:.2f}")
