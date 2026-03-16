from backend.vectorstore.faiss_index import search


def retrieve_medical_knowledge(query):

    results = search(query, k=5)

    return results