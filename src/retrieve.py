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
    '''
    chunk_list is list of dicts, I = list of retrieved vectors
    '''
    retrieved_chunks = [chunk for chunk in chunk_list for i in I
                        if chunk['chunk_id'] == i]

    return retrieved_chunks