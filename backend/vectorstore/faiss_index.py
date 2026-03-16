from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Store documents
documents = []

# FAISS index
index = None


def build_index(texts):

    global index
    global documents

    documents = texts

    embeddings = model.encode(texts)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))


def search(query, k=3):

    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, k)

    results = [documents[i] for i in indices[0]]

    return results