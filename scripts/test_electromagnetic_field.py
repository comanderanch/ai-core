from scripts.electromagnetic_field import ElectromagneticField

def test_em_field():
    print("[Test] Initializing Electromagnetic Field with strength 1000.0")
    field = ElectromagneticField(field_strength=1000.0)

    print("\n[Test] Detecting internal fluctuation...")
    field.detect_fluctuations()

    print("[Test] Detecting external resistance...")
    field.detect_resistance()

    print("[Test] Balancing field...")
    field.balance_field()

    print("[Test] Applying force...")
    field.apply_force()

    print("\n[Result] Final State:")
    print(f"field_strength: {field.field_strength:.2f}")
    print(f"internal_fluctuation: {field.internal_fluctuation:.2f}")
    print(f"external_resistance: {field.external_resistance:.2f}")

if __name__ == "__main__":
    test_em_field()
