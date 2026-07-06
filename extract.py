#%%
# extract text from raw pdf files using pymupdf

import pymupdf
import os
from tqdm import tqdm

def extract_text_from_pdf(pdf_path):
    '''
    Extract text from pdf and store it as a list of dictionaries,
    with the number of elements as the number of pages in the pdf.
    each element contains the pdf file name, the page number and the text.
    '''

    doc = pymupdf.open(pdf_path)
    text = []

    for i, page in enumerate(doc):
        text.append({
            "pdf_file": os.path.basename(pdf_path),
            "page_number": i + 1,
            "text": page.get_text()
        })
    return text

def pdf_files_list(directory):
    pdf_files = []
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            pdf_files.append(os.path.join(directory, file))
    return pdf_files

for pdf_file in tqdm(pdf_files_list("C:\\Users\\SUMANT\\Documents\\Projects\\data\\raw_pdfs"),
                     desc="Extracting text from PDFs"):
    text = extract_text_from_pdf(pdf_file)
    print(pdf_file.split('\\')[-1], len(text))

    # save each dictionary in the text object in the data\\processed folder
    with open(os.path.join("C:\\Users\\SUMANT\\Documents\\Projects\\data\\processed",
                           os.path.basename(pdf_file.replace(".pdf", ".txt"))),
             "w", encoding="utf-8") as f:
        
        for page_data in text:
            f.write(f"PDF File: {page_data['pdf_file']}\n")
            f.write(f"Page {page_data['page_number']}:\n")
            f.write(page_data['text'] + "\n")