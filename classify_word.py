# classify_word.py

import sys
import joblib
import numpy as np
from tensorflow.keras.models import load_model
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


# Your original feature extraction logic — paste from data-preparation.py
english_frequency = {
    'a': 8.17, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.70, 'f': 2.23, 'g': 2.02,
    'h': 6.09, 'i': 6.97, 'j': 0.15, 'k': 0.77, 'l': 4.03, 'm': 2.41, 'n': 6.75,
    'o': 7.51, 'p': 1.93, 'q': 0.10, 'r': 5.99, 's': 6.33, 't': 9.06, 'u': 2.76,
    'v': 0.98, 'w': 2.36, 'x': 0.15, 'y': 1.97, 'z': 0.07
}

qwerty_positions = {
    'a': (0, 0), 's': (0, 1), 'd': (0, 2), 'f': (0, 3), 'j': (0, 4), 'k': (0, 5),
    'l': (0, 6), ';': (0, 7), 'q': (1, 0), 'w': (1, 1), 'e': (1, 2), 'r': (1, 3),
    't': (1, 4), 'y': (1, 5), 'u': (1, 6), 'i': (1, 7), 'o': (1, 8), 'p': (1, 9)
}

qwerty_layout = {
    'home_row': set("asdfjkl;"),
    'bonus_sequences': {'ck': 5, 'fu': 10},
    'positions': qwerty_positions
}

def compute_movement_cost(word, positions):
    cost = 0
    for i in range(1, len(word)):
        prev_pos = positions.get(word[i - 1], (0, 0))
        curr_pos = positions.get(word[i], (0, 0))
        cost += abs(curr_pos[0] - prev_pos[0]) + abs(curr_pos[1] - prev_pos[1])
    return cost

def extract_features(word):
    word = word.lower()
    home_row_score = sum(5 for letter in word if letter in qwerty_layout['home_row'])
    bigram_bonus = sum(qwerty_layout['bonus_sequences'].get(word[i:i+2], 0) * 2 for i in range(len(word)-1))
    frequency_score = sum(english_frequency.get(letter, 0) * 3 for letter in word)
    movement_cost = compute_movement_cost(word, qwerty_layout['positions'])
    return [home_row_score, bigram_bonus, frequency_score, movement_cost]

# Load model and scaler
model = load_model('keyboard_layout_classifier.keras')
scaler = joblib.load('scaler.pkl')

def classify(word):
    features = extract_features(word)
    scaled = scaler.transform([features])
    prob = model.predict(scaled, verbose=0)[0][0]
    label = "Dvorak" if prob > 0.5 else "QWERTY"
    print(f"'{word}' → {label} ({prob:.2f})")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python classify_word.py <word>")
    else:
        classify(sys.argv[1])

