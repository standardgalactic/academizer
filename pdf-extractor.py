import os
import glob
from pdfminer.high_level import extract_text

def extract_pages_text(pdf_file, start_page, end_page):
    page_numbers = range(start_page, end_page)
    text = extract_text(pdf_file, page_numbers=page_numbers)
    return text

def process_pdf(pdf_file):
    # Extract text from the first 100 pages
    extracted_text = extract_pages_text(pdf_file, 0, 100)

    # Create a text file with the same name as the PDF
    base_name = os.path.splitext(pdf_file)[0]
    text_file = f"{base_name}.txt"

    # Write the extracted text to the text file
    with open(text_file, 'w', encoding='utf-8') as file:
        file.write(extracted_text)
    print(f"Processed {pdf_file}")

def get_pdf_files_from_list(file_list):
    # Extract file names from the provided file list
    with open(file_list, 'r') as f:
        files = [line.strip().split("'")[1] for line in f.readlines()]
    return files

# Change this to the path of your 'unconverted-pdfs.txt' file
file_list_path = 'unconverted-pdfs.txt'
pdf_files = get_pdf_files_from_list(file_list_path)

# Process each PDF file
for pdf_file in pdf_files:
    process_pdf(pdf_file)

