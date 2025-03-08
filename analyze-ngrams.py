import os
import re
from collections import Counter
from itertools import islice

def find_files(directory, pattern):
    """Recursively find all files matching the given pattern in the directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if re.search(pattern, file):
                yield os.path.join(root, file)

def tokenize(text):
    """Tokenize the text into words."""
    words = re.findall(r'\w+', text.lower())
    return words

def ngrams(words, n):
    """Generate n-grams from the list of words."""
    return zip(*[islice(words, i, None) for i in range(n)])

def analyze_ngrams(directory, n, top_k=10000):
    """Analyze n-grams in all text files in the directory."""
    ngram_counter = Counter()

    for file_path in find_files(directory, r'\.txt$'):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            words = tokenize(text)
            ngram_counter.update(ngrams(words, n))

    return ngram_counter.most_common(top_k)

def save_ngrams(ngram_counts, n, output_dir):
    """Save the n-grams to a file."""
    output_path = os.path.join(output_dir, f'top_{n}_grams.txt')
    with open(output_path, 'w', encoding='utf-8') as file:
        for ngram, count in ngram_counts:
            file.write(f"{' '.join(ngram)}\t{count}\n")

def main():
    directory = os.getcwd()
    output_dir = os.path.join(directory, 'ngram_results')
    os.makedirs(output_dir, exist_ok=True)

    for n in [2, 3, 4]:
        print(f"Analyzing {n}-grams...")
        ngram_counts = analyze_ngrams(directory, n)
        save_ngrams(ngram_counts, n, output_dir)
        print(f"Top {n}-grams saved to {output_dir}/top_{n}_grams.txt")

if __name__ == "__main__":
    main()