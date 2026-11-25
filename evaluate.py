#%%
import pandas as pd

from src.retrieve import load_faiss_index, retrieve_vectors, retrieve_chunks
from src.embed import embed_text, load_chunk_from_json, get_embedding_model
from tqdm import tqdm

index = load_faiss_index()
merged = load_chunk_from_json("data/vector_db/merged.json")
model = get_embedding_model()

def retrieve(question):
    query_embedding = embed_text(question, model).reshape((1,384))
    I = retrieve_vectors(query_embedding, index, k=5)    
    my_chunks = retrieve_chunks(merged, I)
    return my_chunks

evaluation_results = []
#%%
df = pd.read_csv('data/fin_reg_ai_75_question_evaluation_dataset.csv')
for _, row in tqdm(df.iterrows()):
    question = row['question']
    retrieved_chunks = retrieve(question)

    evaluation_results.append({
        "id": row["id"],
        "question": row["question"],
        "retrieved_chunks": retrieved_chunks,
        "expected_documents": row["expected_documents"],
        "category": row["category"],
        "difficulty": row["difficulty"],
        "answerable": row["answerable"],
        "reference_answer": row["reference_answer"],
        "evidence_keywords": row["evidence_keywords"],
    })

evaluation_results_df = pd.DataFrame(evaluation_results,
                                     columns=['id', 'question',
                                              'retrieved_chunks',
                                              'expected_documents',
                                              'category', 'difficulty',
                                              'answerable', 'reference_answer',
                                              'evidence_keywords'])
evaluation_results_df.to_csv('data/fin_reg_ai_75_question_evaluation_results_v2.csv', index=False)
#%%
import json
from tqdm import tqdm

with open('data/vector_db/merged.json', 'r') as f:
    merged = json.load(f)
#%%

keywords_to_search = ['sensitivity analysis', 'stress testing', "robust", 'extreme values']

new_dict = {}

for keyword in tqdm(keywords_to_search):
    applicable_chunks = []
    # merged is the list of dictionaries read from merged.json
    for dictionary in merged: 
        if keyword in dictionary['text'].lower():
            relevant_statements = [s for s in dictionary['text'].split('.')
                                   if keyword in s.lower()]

            applicable_chunks.append(dict(
                chunk_id=dictionary['chunk_id'],
                document_name=dictionary['document_name'],
                page_numbers=dictionary['page_numbers'],
                relevant_statement=relevant_statements[0] if relevant_statements
                    else dictionary['text']
            ))
    new_dict[keyword] = applicable_chunks

with open('data/keyword_to_applicable_chunks.json', 'w') as f:
    json.dump(new_dict, f, indent=4)

# inspection queries have our original SR-03 question where the model fucked up,
# followed by four simpler questions. The relevant keywords for that query 
# have been added as well.

inspection_queries = [
    ["How does SR 11-7 distinguish sensitivity analysis from stress testing?", ['sensitivity analysis', 'stress testing']],
    ["What is sensitivity analysis in model validation?", ['sensitivity analysis']],
    ["How do small changes in model inputs and parameters affect model outputs?",['sensitivity analysis']],
    ["How does stress testing assess model robustness under extreme inputs?", ['stress testing']],
    ["Compare sensitivity analysis and stress testing in model validation.", ['sensitivity analysis', 'stress testing']]
                    ]

sensitivity_analysis_chunks = new_dict['sensitivity analysis']
stress_testing_chunks = new_dict['stress testing']

def give_score(chunk_ids_retrieved, chunk_ids_to_check):
    score = 0

    for id in chunk_ids_retrieved:
        if id in chunk_ids_to_check:
            score += 1
    return score 
#%%
inspection_results = []
for entry in inspection_queries:
    query = entry[0]
    relevant_keywords = entry[1]

    retrieved_chunks = retrieve(query)
    
    for word in relevant_keywords:
        if word == 'sensitivity analysis':
            chunk_ids_to_check = [dic['chunk_id'] for dic in stress_testing_chunks]
        if word == 'sensitivity analysis':
            chunk_ids_to_check = [dic['chunk_id'] for dic in sensitivity_analysis_chunks]

        chunk_ids_retrieved=[chunk['chunk_id'] for chunk in retrieved_chunks]

        inspection_results.append(dict(
            query=query,
            relevant_keywords=word,
            chunk_ids_retrieved=chunk_ids_retrieved,
            score=give_score(chunk_ids_retrieved, chunk_ids_to_check)
            ))

print(inspection_results)
# %%
import numpy as np
import pandas as pd

def retrieve_vectors(query_embedding, index, k=10):
    """
    Returns FAISS vector positions and their L2 distances.
    Lower distance = more similar.
    """
    distances, indices = index.search(query_embedding, k)

    return indices.tolist()[0], distances.tolist()[0]


def retrieve_chunks(chunk_list, indices, distances):
    """
    chunk_list: chunks in the same order used to build FAISS index
    indices: FAISS vector positions
    distances: corresponding L2 distances
    """
    retrieved_chunks = []

    for rank, (idx, distance) in enumerate(
        zip(indices, distances), start=1
    ):
        if 0 <= idx < len(chunk_list):
            chunk = chunk_list[idx].copy()

            chunk["retrieval_rank"] = rank
            chunk["faiss_distance"] = float(distance)

            retrieved_chunks.append(chunk)

    return retrieved_chunks


def retrieve(question, k=10):
    query_embedding = embed_text(question, model)

    # FAISS expects a 2D float32 array
    query_embedding = np.asarray(
        query_embedding, dtype="float32"
    ).reshape(1, -1)

    indices, distances = retrieve_vectors(
        query_embedding, index, k=k
    )

    my_chunks = retrieve_chunks(
        merged, indices, distances
    )

    return my_chunks


inspection_queries = [
    "How does SR 11-7 distinguish sensitivity analysis from stress testing?",
    "Compare sensitivity analysis and stress testing in model validation.",
    "How does sensitivity analysis differ from stress testing?",
    "According to SR 11-7, what is sensitivity analysis and what is stress testing?",
    "In SR 11-7, how do small changes in model inputs differ from testing across extreme input values?",
    "What does SR 11-7 say about sensitivity analysis, stress testing, and model robustness?"
]

TARGET_CHUNK_ID = 1687
TOP_K = 10

experiment_results = []
retrieved_chunks_data = []
#%%
experiment_results = []
retrieved_chunks_data = []

controlled_queries = [
    # Baseline: original question
    "How does SR 11-7 distinguish sensitivity analysis from stress testing?",

    # Remove document identifier only
    "How does one distinguish sensitivity analysis from stress testing?",

    # Change distinguish to compare
    "How does SR 11-7 compare sensitivity analysis with stress testing?",

    # Add model validation context
    "How does sensitivity analysis differ from stress testing in model validation?",

    # Known successful formulation (control)
    "Compare sensitivity analysis and stress testing in model validation.",

    # Use terminology close to the source passage
    "How do small changes in inputs and parameter values differ from testing across a wide range of inputs, including extreme values?"
]

final_queries = [
    "How does sensitivity analysis differ from stress testing?",

    "How does sensitivity analysis differ from stress testing in model validation?",

    "How does sensitivity analysis differ from stress testing in banking?",

    "How does sensitivity analysis differ from stress testing when assessing model performance?"
]

for query_number, question in enumerate(final_queries, start=1):

    print(f"\nRunning query {query_number}: {question}")

    retrieved_chunks = retrieve(question, k=TOP_K)

    # Store information about every retrieved chunk
    for chunk in retrieved_chunks:

        retrieved_chunks_data.append({
            "query_number": query_number,
            "query": question,
            "rank": chunk["retrieval_rank"],
            "chunk_id": chunk["chunk_id"],
            "document_name": chunk["document_name"],
            "page_numbers": chunk["page_numbers"],
            "faiss_distance": chunk["faiss_distance"]
        })

    # Find the target chunk
    target_match = [
        chunk for chunk in retrieved_chunks
        if chunk["chunk_id"] == TARGET_CHUNK_ID
    ]

    if target_match:
        target = target_match[0]

        target_rank = target["retrieval_rank"]
        target_distance = target["faiss_distance"]
        retrieved = True

    else:
        target_rank = None
        target_distance = None
        retrieved = False

    experiment_results.append({
        "query_number": query_number,
        "query": question,
        "target_chunk_retrieved": retrieved,
        "target_chunk_rank": target_rank,
        "target_chunk_distance": target_distance
    })

    print(f"Target chunk retrieved: {retrieved}")

    if retrieved:
        print(f"Target chunk rank: {target_rank}")
        print(f"Target chunk distance: {target_distance:.4f}")


# Convert results to DataFrames
summary_df_v3 = pd.DataFrame(experiment_results)
details_df_v3 = pd.DataFrame(retrieved_chunks_data)

# Save results
summary_df_v3.to_csv(
    "sr03_experiment_summary_v3.csv",
    index=False
)

details_df_v3.to_csv(
    "sr03_experiment_retrieval_details_v3.csv",
    index=False
)

print("\nDetailed controlled retrieval results saved.")
#%%
# Create a lookup dictionary using chunk IDs
merged_by_id = {
    chunk["chunk_id"]: chunk
    for chunk in merged
}

# Inspect the top five chunks for queries 1 and 2
for query_number in [1, 2]:

    print("\n" + "=" * 100)
    print(f"QUERY {query_number}")
    print("=" * 100)

    query_results = (
        details_df_v2[details_df_v2["query_number"] == query_number]
        .sort_values("rank")
        .head(5)
    )

    for _, result in query_results.iterrows():

        chunk_id = int(result["chunk_id"])
        chunk = merged_by_id[chunk_id]

        print(
            f"\nRank: {result['rank']} | "
            f"Chunk ID: {chunk_id} | "
            f"Document: {result['document_name']} | "
            f"Pages: {result['page_numbers']} | "
            f"Distance: {result['faiss_distance']:.4f}"
        )

        print(chunk["text"])
        print("-" * 100)
#%%
import faiss

# Meaningful titles for each source document
document_titles = {
    "PRA SS1-23.pdf":
        "PRA Supervisory Statement SS1/23: Model Risk Management Principles for Banks",

    "EBA Report on IRB modelling practices.pdf":
        "European Banking Authority Report on IRB Modelling Practices",

    "IFRS 9 Financial Instruments.pdf":
        "International Financial Reporting Standard IFRS 9: Financial Instruments",

    "SR11-7.pdf":
        "Federal Reserve and OCC Supervisory Guidance on Model Risk Management (SR 11-7)",

    "BaselFramework.pdf":
        "Basel Committee on Banking Supervision Basel Framework",
}


def build_augmented_index(chunks, prefix_type):
    """
    Builds a FAISS index using either:
    - filename + original chunk text
    - descriptive document title + original chunk text

    The original chunk dictionaries are not modified.
    """

    embedding_texts = []

    for chunk in chunks:
        document_name = chunk["document_name"]

        if prefix_type == "filename":
            prefix = document_name

        elif prefix_type == "title":
            prefix = document_titles[document_name]

        else:
            raise ValueError("prefix_type must be 'filename' or 'title'")

        embedding_texts.append(
            f"Document: {prefix}\n\n{chunk['text']}"
        )

    embeddings = model.encode(
        embedding_texts,
        batch_size=32,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    new_index = faiss.IndexFlatL2(embeddings.shape[1])
    new_index.add(embeddings)

    assert new_index.ntotal == len(chunks)

    return new_index


# Build the two experimental indexes
filename_index = build_augmented_index(merged, "filename")
title_index = build_augmented_index(merged, "title")

print("Baseline index:", index.ntotal)
print("Filename index:", filename_index.ntotal)
print("Title index:", title_index.ntotal)
#%%
test_queries = [
    "How does sensitivity analysis differ from stress testing?",

    "How does sensitivity analysis differ from stress testing in model validation?",

    "How does sensitivity analysis differ from stress testing in banking?",

    "How does sensitivity analysis differ from stress testing when assessing model performance?",

    "According to SR 11-7, how does sensitivity analysis differ from stress testing?",

    "What distinction does SR 11-7 make between sensitivity analysis and stress testing?"
]


def retrieve_from_index(question, faiss_index, k=10):

    query_embedding = model.encode(
        question,
        convert_to_numpy=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    ).reshape(1, -1)

    distances, indices = faiss_index.search(query_embedding, k)

    results = []

    for rank, (idx, distance) in enumerate(
        zip(indices[0], distances[0]), start=1
    ):
        if 0 <= idx < len(merged):
            chunk = merged[idx]

            results.append({
                "rank": rank,
                "chunk_id": chunk["chunk_id"],
                "document_name": chunk["document_name"],
                "faiss_distance": float(distance)
            })

    return results


indexes = {
    "baseline": index,
    "filename_augmented": filename_index,
    "title_augmented": title_index
}

summary_results = []
detailed_results = []

TARGET_CHUNK_ID = 1687

for query_number, query in enumerate(test_queries, start=1):

    for index_name, faiss_index in indexes.items():

        results = retrieve_from_index(query, faiss_index, k=10)

        target_result = next(
            (
                result for result in results
                if result["chunk_id"] == TARGET_CHUNK_ID
            ),
            None
        )

        summary_results.append({
            "query_number": query_number,
            "query": query,
            "index_type": index_name,
            "target_chunk_retrieved": target_result is not None,
            "target_chunk_rank": (
                target_result["rank"] if target_result else None
            ),
            "target_chunk_distance": (
                target_result["faiss_distance"]
                if target_result else None
            )
        })

        for result in results:
            detailed_results.append({
                "query_number": query_number,
                "query": query,
                "index_type": index_name,
                **result
            })


summary_df = pd.DataFrame(summary_results)
details_df = pd.DataFrame(detailed_results)

summary_df.to_csv(
    "sr03_document_name_experiment_summary.csv",
    index=False
)

details_df.to_csv(
    "sr03_document_name_experiment_details.csv",
    index=False
)

print(summary_df.to_string(index=False))
#%%
faiss.write_index(filename_index, "data/vector_db/regulations_filename.index")
faiss.write_index(title_index, "data/vector_db/regulations_title.index")
