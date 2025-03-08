from pdfminer.high_level import extract_text

def extract_first_page_text(pdf_file, start_page, end_page):
    # Extract text from the first page
    page_numbers = range(start_page, end_page) 
    text = extract_text(pdf_file, page_numbers=page_numbers)
    return text

 # Replace 'input.pdf' with your PDF file name
page_text = extract_first_page_text('input.pdf', 0, 100)

print(page_text)



