#%%
# use BAAI/bge-small-en-v1.5 to convert the text in each chunk into embedding
# and then save it to faiss vector database

import sentence_transformers
import faiss
import numpy as np
import json

def load_chunk_from_json(file_path):
    with open(file_path, 'r') as f:
        chunks = json.load(f)
    return chunks

def get_embedding_model():
    model_name = "BAAI/bge-small-en-v1.5"
    model = sentence_transformers.SentenceTransformer(model_name)
    return model

def embed_text(text, model=None):
    if model is None:
        model = get_embedding_model()
    embedding = model.encode(text)
    return embedding

def embed_chunks(chunks, model=None):
    embeddings = []
    if model is None:
        model = get_embedding_model()
    for chunk in chunks:
        embedding = embed_text(chunk['text'], model)
        embeddings.append(embedding)
    return embeddings

def create_faiss_index(embedding_dimension):
    # Create a FAISS index
    faiss_index = faiss.IndexFlatL2(embedding_dimension)
    return faiss_index

def save_embeddings_to_faiss(embeddings, faiss_index):

    # Convert embeddings to numpy array
    embeddings_array = np.array(embeddings).astype('float32')

    # Add embeddings to the FAISS index
    faiss_index.add(embeddings_array)
#%%
if __name__ == '__main__':
    model = get_embedding_model()
    
    # create one faiss index for all the chunks for all the files in the data/processed folder
    faiss_index = create_faiss_index(384)
    merged_chunks = load_chunk_from_json("data/vector_db/merged.json")
    embeddings = embed_chunks(merged_chunks, model)
    save_embeddings_to_faiss(embeddings, faiss_index)
    faiss.write_index(faiss_index, "data/vector_db/regulations.index")