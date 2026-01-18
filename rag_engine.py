from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma

# Direct import for RetrievalQA is strictly in 'langchain' package, not community/core.
# If that fails, we build the chain manually using LCEL (LangChain Expression Language)
# which is the modern standard.

def process_document(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(texts, embeddings)
    return vector_store

def chat_with_doc(vector_store, query):
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)
    
    # Modern LCEL Approach (No 'chains' module needed)
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain_core.prompts import ChatPromptTemplate

    retriever = vector_store.as_retriever()
    
    prompt = ChatPromptTemplate.from_template("""
    Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}
    """)

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    response = retrieval_chain.invoke({"input": query})
    return response["answer"]