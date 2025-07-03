#training_pairs = [
#    (10, 25),  # Red -> Hot
#    (15, 30),  # Blue -> Cold
#    (20, 35),  # Green -> Growth
#    (40, 60),  # Yellow -> Light
#    (50, 70),  # Black -> Shadow
#]

#above is the original training_pairs.py

#_________________________________________

# training/training_from_csv.py

from training.training_loader import load_training_data

training_data = load_training_data("/root/ai-core/training/training_set.csv")
