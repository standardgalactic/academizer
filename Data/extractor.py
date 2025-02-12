from bs4 import BeautifulSoup
import glob
import os

def extract_text_from_mhtml(mhtml_file):
    encodings = ['utf-8', 'iso-8859-1', 'windows-1252']  # Common web encodings
    for encoding in encodings:
        try:
            with open(mhtml_file, 'r', encoding=encoding) as file:
                content = file.read()
                soup = BeautifulSoup(content, 'html.parser')
                return soup.get_text()
        except UnicodeDecodeError:
            pass
    # If all specified encodings fail, try reading with 'latin1' which won't produce decoding errors
    with open(mhtml_file, 'r', encoding='latin1') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        return soup.get_text()

def process_mhtml(mhtml_file):
    extracted_text = extract_text_from_mhtml(mhtml_file)
    base_name = os.path.splitext(mhtml_file)[0]
    text_file = f"{base_name}.txt"
    with open(text_file, 'w', encoding='utf-8') as file:
        file.write(extracted_text)
    print(f"Processed {mhtml_file}")

mhtml_files = glob.glob('*.mhtml')
for mhtml_file in mhtml_files:
    process_mhtml(mhtml_file)
