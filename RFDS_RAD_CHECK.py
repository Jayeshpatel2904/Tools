import PyPDF2

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        num_pages = pdf_reader.numPages

        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()

    return text

pdf_file_path = r'C:\\Users\\jayeshkumar.patel\\Documents\\Market\\FAY\\RFDS\\RF40\\RFDS-CLFAY00596A-Final-20230914-v.1.pdf'

print(pdf_file_path)
text_from_pdf = read_pdf(pdf_file_path)
print(text_from_pdf)