__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import os
from rag_engine import process_document, chat_with_doc

st.set_page_config(page_title="DocuMind AI", page_icon="", layout="wide")

st.title("🤖 DocuMind: Chat with your PDF")
st.markdown("### Powered by RAG & GPT-4")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    
    if st.button("Clear History"):
        st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Upload a PDF and ask me anything about it."}]

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if uploaded_file and not st.session_state.vector_store:
    with st.spinner("Analyzing document..."):
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.vector_store = process_document("temp.pdf")
        st.success("Document processed!")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask a question..."):
    if not api_key:
        st.error("Please provide an OpenAI API Key in the sidebar.")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    if st.session_state.vector_store:
        with st.spinner("Thinking..."):
            response = chat_with_doc(st.session_state.vector_store, prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)
    else:
        with st.chat_message("assistant"):
             st.write("Please upload a document first so I have context!")