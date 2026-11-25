from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

VECTOR_DB_DIR = DATA_DIR / "vector_db"

RAW_PDF_DIR = DATA_DIR / "raw_pdfs"

PROCESSED_PDF_DIR = DATA_DIR / "processed"

MERGED_JSON = VECTOR_DB_DIR / "merged.json"

FAISS_INDEX = VECTOR_DB_DIR / "regulations.index"

FILENAME_INDEX = VECTOR_DB_DIR / "regulations_filename.index"

TITLE_INDEX = VECTOR_DB_DIR / "regulations_title.index"