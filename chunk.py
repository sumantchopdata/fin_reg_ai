#%%
# chunk the extracted text in chunks of 500 words + 100 overlap
# Every chunk should contain metadata:
# Text, Document name, Page number, Chunk ID

# e.g. chunk 1 will have words 1-500, chunk 2 will have words 401-900,
# chunk 3 will have words 801-1300 and so on.

import os
import json

def load_text_from_file(file_path):
    """
    Loads the extracted text file. Returns: list[str]
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()


def parse_document(lines):
    """
    Converts the text file into a structured list of pages.

    Output:
    [
        {
            "document_name": "IAS36.pdf",
            "page_number": 1,
            "text": "...."
        },
        ...
    ]
    """

    pages = []

    current_document = None
    current_page = None
    current_text = []

    for line in lines:

        line = line.strip()
        if not line:
            continue

        # New document
        if line.startswith("PDF File:"):

            # Save previous page before switching documents
            if current_page is not None:
                pages.append({
                    "document_name": current_document,
                    "page_number": current_page,
                    "text": " ".join(current_text)
                })

            current_document = line.replace("PDF File:", "").strip()
            current_page = None
            current_text = []

        # New page
        elif line.startswith("Page") and line.endswith(":"):

            # Save previous page
            if current_page is not None:
                pages.append({
                    "document_name": current_document,
                    "page_number": current_page,
                    "text": " ".join(current_text)
                })

            current_page = int(line.replace("Page", "").replace(":", "").strip())
            current_text = []

        else:
            current_text.append(line)

    # Save final page
    if current_page is not None:
        pages.append({
            "document_name": current_document,
            "page_number": current_page,
            "text": " ".join(current_text)
        })

    return pages


def chunk_pages(pages, chunk_size=500, overlap=100):
    """
    Create overlapping chunks from parsed pages.

    Returns:
    [
        {
            "chunk_id": 0,
            "document_name": "...",
            "page_numbers": [1,2],
            "text": "..."
        }
    ]
    """

    chunks = []

    chunk_id = 0

    current_words = []
    current_pages = []
    current_document = None

    for page in pages:

        words = page["text"].split()

        idx = 0

        while idx < len(words):

            # New document?
            if current_document != page["document_name"]:

                if current_words:
                    chunks.append({
                        "chunk_id": chunk_id,
                        "document_name": current_document,
                        "page_numbers": sorted(set(current_pages)),
                        "text": " ".join(current_words)
                    })

                    chunk_id += 1

                current_document = page["document_name"]
                current_words = []
                current_pages = []

            remaining_space = chunk_size - len(current_words)

            current_words.extend(words[idx: idx + remaining_space])

            current_pages.append(page["page_number"])

            idx += remaining_space

            if len(current_words) >= chunk_size:

                chunks.append({
                    "chunk_id": chunk_id,
                    "document_name": current_document,
                    "page_numbers": sorted(set(current_pages)),
                    "text": " ".join(current_words)
                })

                chunk_id += 1

                # Keep overlap
                current_words = current_words[-overlap:]

                # Overlap belongs to latest page
                current_pages = [page["page_number"]]

    # Save last chunk
    if current_words:

        # Merge tiny final chunk
        if len(current_words) < chunk_size * 0.3 and chunks:

            chunks[-1]["text"] += " " + " ".join(current_words)

            chunks[-1]["page_numbers"] = sorted(
                set(chunks[-1]["page_numbers"] + current_pages)
            )

        else:

            chunks.append({
                "chunk_id": chunk_id,
                "document_name": current_document,
                "page_numbers": sorted(set(current_pages)),
                "text": " ".join(current_words)
            })

    return chunks
#%%
# loop over all the files, create chunks for each file and save them in a json file in the data/processed folder

import os
import json

for file in os.listdir("data/processed"):
    if file.endswith(".txt"):
        lines = load_text_from_file(os.path.join("data/processed", file))
        pages = parse_document(lines)
        chunks = chunk_pages(pages)

        with open(os.path.join("data/processed",
                                file.replace(".txt", "_chunks.json")),
                                "w",
                                encoding="utf-8"
                               ) as f:
            json.dump(chunks, f, indent=4)