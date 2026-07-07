#%%
# test it all out with a new query

from prompting import SYSTEM_PROMPT, user_prompt
from llm import ask_llm
from embed import embed_text, get_embedding_model, load_chunk_from_json
from retrieve import load_faiss_index, retrieve_vectors, retrieve_chunks

model = get_embedding_model()

query = "What is counterparty credit risk?"

query_embedding = embed_text(query).reshape((1,384))

index = load_faiss_index()

I = retrieve_vectors(query_embedding, index, k=5)
print(I)
merged = load_chunk_from_json('data/vector_db/merged.json')
print(len(merged))

my_chunks = retrieve_chunks(merged, I)

u_prompt = user_prompt(my_chunks, query)
print(len(u_prompt), len(SYSTEM_PROMPT))
#%%
answer = ask_llm(u_prompt)
print(answer)
# %%
