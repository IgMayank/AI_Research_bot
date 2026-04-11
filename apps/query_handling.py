from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from data_retrieval import retrieve_data
from data_ingestion import process_document

UPLOAD_PATH = "../Data"


if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

if "agent" not in st.session_state:
    st.session_state.agent = None


def setup_agent():
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    memory = InMemorySaver()

    @tool
    def rag_tool(query: str):
        """Retrieve relevant context from documents for the given query."""
        docs = retrieve_data(query)
        context = ""
        for doc in docs:
            context += doc.page_content + "\n"
        return context

    system_prompt = """You are an AI research assistant.
You have access to a tool that retrieves relevant document context.

Rules:
1. Use the rag_tool ONLY once per query if needed.
2. After receiving context, generate a final answer immediately.
3. Do NOT call the tool repeatedly.
4. If sufficient information is available, answer directly.
5. If the answer is not found, say: "Answer not found in documents."
"""

    return create_agent(
        model=llm,
        tools=[rag_tool],
        checkpointer=memory,
        system_prompt=system_prompt,
    )



st.title("📄 AI Research Assistant")


if not st.session_state.document_uploaded:
    uploaded = st.file_uploader("Select PDF Files", type=["pdf"], accept_multiple_files=True)
    if uploaded:
        with st.spinner("Processing documents..."):
            os.makedirs(UPLOAD_PATH, exist_ok=True)
            for file in uploaded:
                with open(os.path.join(UPLOAD_PATH, file.name), "wb") as f:
                    f.write(file.getvalue())
            process_document(UPLOAD_PATH)
            st.session_state.agent = setup_agent()
            st.session_state.document_uploaded = True
        st.rerun()


if st.session_state.document_uploaded and st.session_state.agent:
    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])

    query = st.chat_input("Ask anything about your documents...")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        st.chat_message("user").markdown(query)

        response = st.session_state.agent.invoke(
            {"messages": [{"role": "user", "content": query}]},
            config={"configurable": {"thread_id": "abc"}}
        )

        answer = response["messages"][-1].content
        st.chat_message("assistant").markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
