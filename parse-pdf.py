from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

writer.add_page(reader.pages[0])

with open("first_page.pdf", "wb") as output_pdf:
        writer.write(output_pdf)

