#%%
import pandas as pd

df = pd.read_csv('data/fin_reg_ai_75_question_evaluation_dataset.csv')
#%%
# from src.llm import ask_llm
from src.retrieve import load_faiss_index, retrieve_vectors, retrieve_chunks
from src.embed import embed_text, load_chunk_from_json, get_embedding_model
# from src.prompting import user_prompt
from tqdm import tqdm
# import time

index = load_faiss_index()
merged = load_chunk_from_json("data/vector_db/merged.json")
model = get_embedding_model()

def retrieve(question):
    query_embedding = embed_text(question, model).reshape((1,384))
    I = retrieve_vectors(query_embedding, index, k=5)    
    my_chunks = retrieve_chunks(merged, I)
    return my_chunks

# def ask_llm_with_retry(u_prompt, max_retries=5):
#     for attempt in range(max_retries):
#         try:
#             return ask_llm(u_prompt)

#         except Exception as e:
#             if attempt == max_retries - 1:
#                 raise e

#             wait_time = 5 * (2 ** attempt)

#             print(
#                 f"\nLLM request failed. "
#                 f"Retrying in {wait_time}s..."
#             )

#             time.sleep(wait_time)

evaluation_results = []
#%%
for question in tqdm(df.question):
    retrieved_chunks = retrieve(question)
    
    evaluation_results.append([
        question,
        retrieved_chunks,
    ])

evaluation_results_df = pd.DataFrame(evaluation_results, columns=['question', 'retrieved_chunks'])
evaluation_results_df.to_csv('data/fin_reg_ai_75_question_evaluation_results.csv', index=False)
# %%
import pandas as pd
import ast
evaluation_results_df = pd.read_csv('data/fin_reg_ai_75_question_evaluation_results.csv')

for n, retrieved_chunks in enumerate(evaluation_results_df['retrieved_chunks']):
    retrieved_chunks = ast.literal_eval(retrieved_chunks)
    texts = [chunk['text'] for chunk in retrieved_chunks]

    # put 5 texts in 5 separate columns
    for i in range(len(texts)):
        evaluation_results_df.loc[n, f'retrieved_chunk_{i+1}'] = texts[i]
# %%
del evaluation_results_df['retrieved_chunks']
evaluation_results_df.to_csv('data/fin_reg_ai_75_question_evaluation_results_2.csv', index=False)