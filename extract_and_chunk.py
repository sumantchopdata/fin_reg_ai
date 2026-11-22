#%%
from src.extract import extract_text_from_pdf, pdf_files_list
from src.chunk import load_text_from_file, parse_document, chunk_pages
from src.config import MERGED_JSON, PROCESSED_PDF_DIR, RAW_PDF_DIR
from tqdm import tqdm
import os
import json
from pathlib import Path

for pdf_file in tqdm(pdf_files_list(RAW_PDF_DIR),
                    desc="Extracting text from PDFs"):
    text = extract_text_from_pdf(pdf_file)
    print(pdf_file.split('\\')[-1], len(text))

    # save each dictionary in the text object in the data\\processed folder
    output_file = PROCESSED_PDF_DIR / (Path(pdf_file).stem + ".txt")
    with open(output_file, "w", encoding="utf-8") as f:
        for page_data in text:
            f.write(f"PDF File: {page_data['pdf_file']}\n")
            f.write(f"Page {page_data['page_number']}:\n")
            f.write(page_data['text'] + "\n")

#%%
prev_chunks = 0
merged_data = []

for file in tqdm(os.listdir(PROCESSED_PDF_DIR)):
    if file.endswith(".txt"):
        print(f"Processing file: {file}")
        lines = load_text_from_file(os.path.join(PROCESSED_PDF_DIR, file))
        pages = parse_document(lines)
        chunks = chunk_pages(pages, index=prev_chunks)
        for chunk in chunks:
            merged_data.append(chunk)
        prev_chunks += len(chunks)

with open(MERGED_JSON, 'w') as outfile:
    json.dump(merged_data, outfile, indent=4)
#%%
from src.embed import get_embedding_model, embed_chunks, create_faiss_index, save_embeddings_to_faiss, load_chunk_from_json 
from src.config import FAISS_INDEX, MERGED_JSON
import faiss

if __name__ == '__main__':
    model = get_embedding_model()
    
    # create one faiss index for all the chunks for all the files in the data/processed folder
    # and store it in the data/vector_db folder.
    faiss_index = create_faiss_index(384)
    merged_chunks = load_chunk_from_json(MERGED_JSON)
    embeddings = embed_chunks(merged_chunks, model)
    save_embeddings_to_faiss(embeddings, faiss_index)
#%%
if __name__ == '__main__':
    Path(FAISS_INDEX).parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(faiss_index, str(FAISS_INDEX))