import store


def retrieve_data(query: str, k: int = 4):
    if store.vector_store is None:
        raise ValueError("Vector store is empty. Please upload documents first.")
    
    docs = store.vector_store.similarity_search(query, k=k)
    return docs