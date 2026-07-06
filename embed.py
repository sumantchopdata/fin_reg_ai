# use BAAI/bge-small-en-v1.5 to convert the text in each chunk into embedding
# and then save it to faiss vector database

import sentence_transformers
import faiss
import numpy as np

def get_embedding_model():
    model_name = "BAAI/bge-small-en-v1.5"
    model = sentence_transformers.SentenceTransformer(model_name)
    return model

def embed_text(text):
    model = get_embedding_model()
    embedding = model.encode(text)
    return embedding

def embed_chunks(chunks):
    embeddings = []
    for chunk in chunks:
        embedding = embed_text(chunk)
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

