#!/usr/bin/env python3
"""
A script to extract plain text from all PDF and MHTML files in the current directory.
It parses each MHTML file as a MIME message, extracts text from its HTML (or plain text) parts,
removes tags using BeautifulSoup, and writes the results to separate .txt files.

For PDF files, it extracts text using PyMuPDF (fitz) and writes the results to separate .txt files.

Usage: 
    python process_files.py

Ensure you have installed the required libraries (e.g., pip install beautifulsoup4 PyMuPDF)
"""

import glob
import os
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
import fitz  # PyMuPDF

def extract_text_from_mhtml(file_path):
    """
    Extract plain text from an MHTML file by parsing its MIME structure.
    It processes both HTML parts (removing tags) and plain text parts.
    """
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    text_parts = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            # Process HTML content by removing HTML tags
            if (content := part.get_payload(decode=True)) is not None:
                if content_type == 'text/html':
                    soup = BeautifulSoup(content, 'html.parser')
                    text_parts.append(soup.get_text(separator="\n", strip=True))
                # If plain text is available, extract it as well
                elif content_type == 'text/plain':
                    text_parts.append(content.decode('utf-8'))
    else:
        content_type = msg.get_content_type()
        if (content := msg.get_payload(decode=True)) is not None:
            if content_type == 'text/html':
                soup = BeautifulSoup(content, 'html.parser')
                text_parts.append(soup.get_text(separator="\n", strip=True))
            else:
                text_parts.append(content.decode('utf-8'))
    
    return "\n\n".join(text_parts)

def extract_text_from_pdf(file_path):
    """
    Extract plain text from a PDF file using PyMuPDF (fitz).
    """
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def main():
    # Process MHTML files
    mhtml_files = glob.glob("*.mhtml")
    if mhtml_files:
        for file_path in mhtml_files:
            print(f'Processing {file_path} ...')
            extracted_text = extract_text_from_mhtml(file_path)
            output_file = os.path.splitext(file_path)[0] + ".txt"
            with open(output_file, "w", encoding="utf-8") as out:
                out.write(extracted_text)
            print(f"Extracted text written to {output_file}")
    else:
        print("No MHTML files found in the current directory.")
    
    # Process PDF files
    pdf_files = glob.glob("*.pdf")
    if pdf_files:
        for file_path in pdf_files:
            print(f'Processing {file_path} ...')
            extracted_text = extract_text_from_pdf(file_path)
            output_file = os.path.splitext(file_path)[0] + ".txt"
            with open(output_file, "w", encoding="utf-8") as out:
                out.write(extracted_text)
            print(f"Extracted text written to {output_file}")
    else:
        print("No PDF files found in the current directory.")

if __name__ == "__main__":
    main()