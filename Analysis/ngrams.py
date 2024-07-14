import os
import nltk
from nltk.util import ngrams
from collections import Counter

# Function to generate ngrams from a given text
def generate_ngrams(text, n):
    ngrams_list = ngrams(sequence=nltk.word_tokenize(text), n=n)
    return [' '.join(gram) for gram in ngrams_list]

# Get all the .txt files in the current directory
files = [file for file in os.listdir('.') if file.endswith('.txt')]

# Iterate through each file, read it, and generate ngrams
for file in files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
            print(f"File: {file}")

# Generate 3-grams
        ngrams_list = generate_ngrams(text, 3)
        ngrams_counter = Counter(ngrams_list)
        most_common_3grams = ngrams_counter.most_common(10)

        # Print the most common 3-grams
        print("\nTop 10 most common 3-grams:")
        for gram, count in most_common_3grams:
            print(f"{gram}: {count} times")

        print("\n")
    except UnicodeDecodeError:
        print(f"Skipping {file}: Not UTF-8 encoded.\n")
        continue
