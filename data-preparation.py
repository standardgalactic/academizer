#!/c/Users/Mechachleopteryx/AppData/Local/Microsoft/WindowsApps/python3

import csv

# Example frequency values (adjust as needed)
english_frequency = {
    'a': 8.17, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.70, 'f': 2.23, 'g': 2.02,
    'h': 6.09, 'i': 6.97, 'j': 0.15, 'k': 0.77, 'l': 4.03, 'm': 2.41, 'n': 6.75,
    'o': 7.51, 'p': 1.93, 'q': 0.10, 'r': 5.99, 's': 6.33, 't': 9.06, 'u': 2.76,
    'v': 0.98, 'w': 2.36, 'x': 0.15, 'y': 1.97, 'z': 0.07
}

# Example keyboard positions for QWERTY layout
qwerty_positions = {
    'a': (0, 0), 's': (0, 1), 'd': (0, 2), 'f': (0, 3), 'j': (0, 4), 'k': (0, 5),
    'l': (0, 6), ';': (0, 7), 'q': (1, 0), 'w': (1, 1), 'e': (1, 2), 'r': (1, 3),
    't': (1, 4), 'y': (1, 5), 'u': (1, 6), 'i': (1, 7), 'o': (1, 8), 'p': (1, 9)
}

# Example keyboard positions for Dvorak layout
dvorak_positions = {
    'a': (0, 0), 'o': (0, 1), 'e': (0, 2), 'u': (0, 3), 't': (0, 4), 'h': (0, 5),
    'n': (0, 6), 's': (0, 7), 'q': (1, 0), 'j': (1, 1), 'k': (1, 2), 'x': (1, 3),
    'b': (1, 4), 'm': (1, 5), 'w': (1, 6), 'v': (1, 7), 'z': (1, 8), 'y': (1, 9)
}

def compute_movement_cost(word, positions):
    """
    Compute the movement cost based on the positions of keys in a layout.
    """
    cost = 0
    for i in range(1, len(word)):
        prev_pos = positions.get(word[i - 1], (0, 0))
        curr_pos = positions.get(word[i], (0, 0))
        cost += abs(curr_pos[0] - prev_pos[0]) + abs(curr_pos[1] - prev_pos[1])
    return cost

def generate_dataset(word_list, layout):
    """
    Generate dataset with features extracted from words, rounded to integers.
    """
    dataset = []
    for word in word_list:
        home_row_score = sum(5 for letter in word if letter in layout['home_row'])
        bigram_bonus = sum(layout['bonus_sequences'].get(seq, 0) * 2 for seq in layout['bonus_sequences'] if seq in word)
        frequency_score = sum(english_frequency.get(letter, 0) * 3 for letter in word)
        movement_cost = compute_movement_cost(word, layout['positions'])
        dataset.append([word, round(home_row_score), round(bigram_bonus), round(frequency_score), round(movement_cost)])
    return dataset

def read_word_list(file_path):
    """
    Read a list of words from a file.
    """
    with open(file_path, 'r') as file:
        word_list = [line.strip() for line in file.readlines()]
    return word_list

# Read word list from file
word_list = read_word_list('top-10000-english-words')

# QWERTY layout
qwerty = {
    'home_row': set("asdfjkl;"),
    'bonus_sequences': {'ck': 5, 'fu': 10},
    'positions': qwerty_positions
}

# Dvorak layout
dvorak = {
    'home_row': set("aoeuthns"),
    'bonus_sequences': {'th': 5, 'an': 8},
    'positions': dvorak_positions
}

# Generate datasets for QWERTY and Dvorak layouts
qwerty_dataset = generate_dataset(word_list, qwerty)
dvorak_dataset = generate_dataset(word_list, dvorak)

# Save datasets to CSV
with open('qwerty_dataset.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['word', 'home_row_score', 'bigram_bonus', 'frequency_score', 'movement_cost'])
    writer.writerows(qwerty_dataset)

with open('dvorak_dataset.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['word', 'home_row_score', 'bigram_bonus', 'frequency_score', 'movement_cost'])
    writer.writerows(dvorak_dataset)
