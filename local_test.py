#%%
# test it all out with a new query

from prompting import SYSTEM_PROMPT, user_prompt
from llm import ask_llm
from embed import embed_text, load_chunk_from_json
from retrieve import load_faiss_index, retrieve_vectors, retrieve_chunks
from dotenv import load_dotenv
import os
from google import genai
import streamlit as st

load_dotenv()

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

# model = get_embedding_model()

index = load_faiss_index()
#%%
query = "What is the Look-through approach in the context of market risk?"

query_embedding = embed_text(query).reshape((1,384))

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
