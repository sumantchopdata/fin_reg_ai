#%%
# function for retrieval

import sentence_transformers
import faiss

def get_embedding_model():
    model_name = "BAAI/bge-small-en-v1.5"
    model = sentence_transformers.SentenceTransformer(model_name)
    return model

def embed_text(text, model=None):
    if model is None:
        model = get_embedding_model()
    embedding = model.encode(text)
    return embedding

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