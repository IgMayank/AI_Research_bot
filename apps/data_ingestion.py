from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
import store
import os


def process_document(path):
    # loader
    loader = PyPDFDirectoryLoader(path)
    docs = loader.load()

    # split
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=250)
    splitted_chunks = splitter.split_documents(documents=docs)
    for i, chunk in enumerate(splitted_chunks):
        chunk.metadata["chunk_id"] = i
        if 'source' in chunk.metadata:
            chunk.metadata["source"] = os.path.basename(chunk.metadata["source"])

    # embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

  
    store.vector_store = InMemoryVectorStore.from_documents(
        documents=splitted_chunks,
        embedding=embeddings,
    )
