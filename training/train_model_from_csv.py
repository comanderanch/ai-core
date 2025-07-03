# training/train_model_from_csv.py

from training.training_from_csv import training_data

def run_training():
    print("=== AI-Core Minimal Model Training (CSV Mode) ===")
    for input_token, target_token, label, weight in training_data:
        print(f"[TRAINING] {input_token} ➡ {target_token} | Label: '{label}' | Weight: {weight}")

if __name__ == "__main__":
    run_training()

#test it in terminal with line 14
#python3 training/train_model_from_csv.py
