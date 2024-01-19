from bs4 import BeautifulSoup
import glob
import os

def extract_text_from_mhtml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        return soup.get_text()

# Path to the directory containing MHTML files
directory_path = "$PWD"

# Iterate over all MHTML files in the directory
for file_path in glob.glob(os.path.join(directory_path, '*.mhtml')):
    text = extract_text_from_mhtml(file_path)
    base_name = os.path.splitext(file_path)[0]
    text_file = f"{base_name}.txt"
    with open(text_file, 'w', encoding='utf-8') as file:
        file.write(text)

