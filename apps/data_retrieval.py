from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
# from query_handling import query

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={
        "normalize_embeddings": True
    })
vector_store = Chroma(
        persist_directory="./vector_store_",
        embedding_function=embeddings,)


def retrieve_data(query:str , k:int=4):
    
    docs = vector_store.similarity_search(query , k=k)

    return docs










# @tool
# def retrieve_data(query):
#     """ Use this tool when u need additional information from documents 
#     """
#     # embeddings = HuggingFaceEmbeddings(
#     #     model_name="all-MiniLM-L6-v2"
#     # )

#     embeddings = HuggingFaceEmbeddings(
#     model_name="BAAI/bge-base-en-v1.5",
#     model_kwargs={"device": "cpu"},
#     encode_kwargs={
#         "normalize_embeddings": True
#     }
# )
#     # load exixsting db
#     vector_store = Chroma(
#         persist_directory="./vector_store_",
#         embedding_function=embeddings,
#     )
#     # retrival of top k
#     docs = vector_store.similarity_search(query , k=4)

#     return docs

# results = retrieve_data(query)




        