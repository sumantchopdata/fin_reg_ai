#%%
# function for retrieval

import faiss
import streamlit as st

@st.cache_resource
def load_faiss_index():
    index = faiss.read_index("data/vector_db/regulations.index")
    return index

def retrieve_vectors(query_embedding, index, k=3):
    _, I = index.search(query_embedding, k)
    return I.tolist()[0]

def retrieve_chunks(chunk_list, I):
    """
    chunk_list: list of chunks in the same order used to build FAISS index
    I: FAISS vector positions
    """

    retrieved_chunks = [chunk_list[i] for i in I if 0 <= i < len(chunk_list)]

    return retrieved_chunks