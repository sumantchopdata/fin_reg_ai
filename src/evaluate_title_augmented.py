#%%

import json
import numpy as np
import pandas as pd
from pathlib import Path
from src.embed import load_chunk_from_json, get_embedding_model
from src.retrieve import load_faiss_index

# ============================================================
# CONFIGURATION
# ============================================================

EVALUATION_FILE = Path(
    "data/fin_reg_ai_75_question_evaluation_dataset.json"
)

OUTPUT_DIR = Path("evaluation_title_augmented")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TOP_K = 5

# ============================================================
# VALIDATION
# ============================================================

merged = load_chunk_from_json("data/vector_db/merged.json")
model = get_embedding_model()
title_index = load_faiss_index(config='title')

assert len(merged) == title_index.ntotal, (
    f"Chunk/index mismatch: {len(merged)} chunks vs "
    f"{title_index.ntotal} vectors"
)

assert EVALUATION_FILE.exists(), (
    f"Evaluation file not found: {EVALUATION_FILE}"
)

with open(EVALUATION_FILE, "r", encoding="utf-8") as f:
    evaluation_data = json.load(f)

print(f"Loaded {len(evaluation_data)} evaluation questions.")
print(f"Loaded {len(merged)} chunks.")
print(f"FAISS index contains {title_index.ntotal} vectors.")


# ============================================================
# DOCUMENT NAME NORMALISATION
# ============================================================

def normalise_document_name(name):
    """
    Normalises document names to avoid accidental partial
    matching, e.g. confusing PRA with EBA IRB.
    """
    return Path(name).name.strip().lower()


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve_from_title_index(question, k=TOP_K):

    query_embedding = model.encode(
        question,
        convert_to_numpy=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    ).reshape(1, -1)

    distances, indices = title_index.search(
        query_embedding, k
    )

    retrieved_chunks = []

    for rank, (idx, distance) in enumerate(
        zip(indices[0], distances[0]), start=1
    ):

        if idx < 0 or idx >= len(merged):
            continue

        # Original chunk, NOT the title-augmented embedding text
        chunk = merged[idx]

        retrieved_chunks.append({
            "rank": rank,
            "chunk_id": chunk["chunk_id"],
            "document_name": chunk["document_name"],
            "page_numbers": chunk["page_numbers"],
            "text": chunk["text"],
            "faiss_distance": float(distance)
        })

    return retrieved_chunks


# ============================================================
# EVALUATION
# ============================================================

retrieval_details = []
question_summary = []

for question_number, item in enumerate(evaluation_data, start=1):

    question_id = item["id"]
    question = item["question"]

    expected_documents = {
        normalise_document_name(doc)
        for doc in item["expected_documents"]
    }

    answerable = item["answerable"]

    print(
        f"[{question_number}/{len(evaluation_data)}] "
        f"Processing {question_id}: {question}"
    )

    retrieved_chunks = retrieve_from_title_index(
        question,
        k=TOP_K
    )

    retrieved_documents = {
        normalise_document_name(chunk["document_name"])
        for chunk in retrieved_chunks
    }

    # --------------------------------------------------------
    # Document-level coverage
    # --------------------------------------------------------

    matched_documents = (
        expected_documents.intersection(retrieved_documents)
    )

    all_expected_retrieved = (
        expected_documents.issubset(retrieved_documents)
        if answerable else None
    )

    at_least_one_expected_retrieved = (
        len(matched_documents) > 0
        if answerable else None
    )

    # --------------------------------------------------------
    # Keyword coverage
    # --------------------------------------------------------

    evidence_keywords = item.get("evidence_keywords", [])

    retrieved_text = " ".join(
        chunk["text"] for chunk in retrieved_chunks
    ).lower()

    matched_keywords = [
        keyword for keyword in evidence_keywords
        if keyword.lower() in retrieved_text
    ]

    keyword_coverage = (
        len(matched_keywords) / len(evidence_keywords)
        if evidence_keywords else None
    )

    # --------------------------------------------------------
    # Question-level summary
    # --------------------------------------------------------

    question_summary.append({

        "id": question_id,
        "question": question,

        "category": item["category"],
        "difficulty": item["difficulty"],
        "answerable": answerable,

        "expected_documents": "; ".join(
            item["expected_documents"]
        ),

        "retrieved_documents": "; ".join(sorted(
            {
                chunk["document_name"]
                for chunk in retrieved_chunks
            }
        )),

        "matched_expected_documents": "; ".join(sorted(
            matched_documents
        )),

        "expected_document_count": len(expected_documents),

        "matched_document_count": len(matched_documents),

        "all_expected_documents_retrieved":
            all_expected_retrieved,

        "at_least_one_expected_document_retrieved":
            at_least_one_expected_retrieved,

        "evidence_keyword_count": len(evidence_keywords),

        "matched_keyword_count": len(matched_keywords),

        "matched_keywords": "; ".join(matched_keywords),

        "keyword_coverage": keyword_coverage

    })

    # --------------------------------------------------------
    # Individual retrieved chunks
    # --------------------------------------------------------

    for chunk in retrieved_chunks:

        retrieval_details.append({

            "id": question_id,
            "question": question,

            "category": item["category"],
            "difficulty": item["difficulty"],
            "answerable": answerable,

            "expected_documents": "; ".join(
                item["expected_documents"]
            ),

            "retrieval_rank": chunk["rank"],

            "chunk_id": chunk["chunk_id"],

            "document_name": chunk["document_name"],

            "page_numbers": "; ".join(
                map(str, chunk["page_numbers"])
            ),

            "faiss_distance": chunk["faiss_distance"],

            "chunk_text": chunk["text"]

        })


# ============================================================
# SAVE RAW RESULTS
# ============================================================

summary_df = pd.DataFrame(question_summary)

details_df = pd.DataFrame(retrieval_details)

summary_df.to_csv(
    OUTPUT_DIR / "title_augmented_question_summary.csv",
    index=False
)

details_df.to_csv(
    OUTPUT_DIR / "title_augmented_retrieval_details.csv",
    index=False
)

print("\nRaw evaluation results saved.")


# ============================================================
# AGGREGATE METRICS
# ============================================================

answerable_df = summary_df[
    summary_df["answerable"] == True
].copy()

unanswerable_df = summary_df[
    summary_df["answerable"] == False
].copy()


def calculate_metrics(df):

    total = len(df)

    if total == 0:
        return {
            "total_questions": 0,
            "full_document_coverage": None,
            "partial_document_coverage": None,
            "average_keyword_coverage": None
        }

    return {

        "total_questions": total,

        "full_document_coverage": (
            df["all_expected_documents_retrieved"]
            .mean()
        ),

        "partial_document_coverage": (
            df["at_least_one_expected_document_retrieved"]
            .mean()
        ),

        "average_keyword_coverage": (
            df["keyword_coverage"].mean()
        )

    }


overall_metrics = calculate_metrics(answerable_df)


# ============================================================
# SINGLE-DOCUMENT VS CROSS-DOCUMENT
# ============================================================

single_document_df = answerable_df[
    answerable_df["expected_document_count"] == 1
]

cross_document_df = answerable_df[
    answerable_df["expected_document_count"] > 1
]

single_metrics = calculate_metrics(single_document_df)
cross_metrics = calculate_metrics(cross_document_df)


# ============================================================
# DIFFICULTY-WISE METRICS
# ============================================================

difficulty_results = []

for difficulty, group in answerable_df.groupby("difficulty"):

    metrics = calculate_metrics(group)

    difficulty_results.append({
        "difficulty": difficulty,
        **metrics
    })

difficulty_df = pd.DataFrame(difficulty_results)


# ============================================================
# CATEGORY-WISE METRICS
# ============================================================

category_results = []

for category, group in answerable_df.groupby("category"):

    metrics = calculate_metrics(group)

    category_results.append({
        "category": category,
        **metrics
    })

category_df = pd.DataFrame(category_results)


# ============================================================
# DOCUMENT DISTRIBUTION
# ============================================================

document_distribution = (
    details_df["document_name"]
    .value_counts()
    .rename_axis("document_name")
    .reset_index(name="retrieved_chunk_count")
)


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n" + "=" * 65)
print("TITLE-AUGMENTED INDEX: EVALUATION RESULTS")
print("=" * 65)

print(f"\nTotal questions: {len(summary_df)}")
print(f"Answerable questions: {len(answerable_df)}")
print(f"Unanswerable questions: {len(unanswerable_df)}")

print("\nOVERALL ANSWERABLE QUESTION METRICS")

for metric, value in overall_metrics.items():
    print(f"{metric}: {value}")

print("\nSINGLE-DOCUMENT QUESTIONS")

for metric, value in single_metrics.items():
    print(f"{metric}: {value}")

print("\nCROSS-DOCUMENT QUESTIONS")

for metric, value in cross_metrics.items():
    print(f"{metric}: {value}")

print("\nDIFFICULTY-WISE RESULTS")
print(difficulty_df.to_string(index=False))

print("\nCATEGORY-WISE RESULTS")
print(category_df.to_string(index=False))

print("\nDOCUMENT DISTRIBUTION")
print(document_distribution.to_string(index=False))


# ============================================================
# SAVE AGGREGATE METRICS
# ============================================================

difficulty_df.to_csv(
    OUTPUT_DIR / "title_augmented_difficulty_metrics.csv",
    index=False
)

category_df.to_csv(
    OUTPUT_DIR / "title_augmented_category_metrics.csv",
    index=False
)

document_distribution.to_csv(
    OUTPUT_DIR / "title_augmented_document_distribution.csv",
    index=False
)

aggregate_results = {

    "total_questions": len(summary_df),

    "answerable_questions": len(answerable_df),

    "unanswerable_questions": len(unanswerable_df),

    "overall": overall_metrics,

    "single_document": single_metrics,

    "cross_document": cross_metrics

}

with open(
    OUTPUT_DIR / "title_augmented_aggregate_metrics.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        aggregate_results,
        f,
        indent=4
    )

print("\n" + "=" * 65)
print("EVALUATION COMPLETED")
print(f"Results saved in: {OUTPUT_DIR.resolve()}")
print("=" * 65)
