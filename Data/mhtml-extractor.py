import os
import glob
from bs4 import BeautifulSoup

def extract_text_from_mhtml(mhtml_file):
    with open(mhtml_file, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        return soup.get_text()

def process_mhtml(mhtml_file):
# Extract text from the MHTML file
    extracted_text = extract_text_from_mhtml(mhtml_file)

# Create a text file with the same name as the MHTML file
    base_name = os.path.splitext(mhtml_file)[0]
    text_file = f"{base_name}.txt"

# Write the extracted text to the text file
    with open(text_file, 'w', encoding='utf-8') as file:
        file.write(extracted_text)
    print(f"Processed {mhtml_file}")

# Get all MHTML files in the current working directory
mhtml_files = glob.glob('*.mhtml')

# Process each MHTML file
for mhtml_file in mhtml_files:
    process_mhtml(mhtml_file)

