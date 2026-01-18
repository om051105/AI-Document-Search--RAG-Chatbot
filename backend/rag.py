import os
from typing import List
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables (API keys)
load_dotenv()

# CORE CONFIGURATION
CHROMA_DB_DIR = "chroma_db"
COLLECTION_NAME = "my_rag_collection"

class RAGService:
    def __init__(self):
        """
        Initialize the RAG Service.
        """
        # 1. Embeddings
        self.embedding_function = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

        # 2. Vector Store
        self.vector_store = Chroma(
            persist_directory=CHROMA_DB_DIR,
            embedding_function=self.embedding_function,
            collection_name=COLLECTION_NAME
        )

        # 3. LLM
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0
        )
        
        # 4. Retriever
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )

    def add_pdf_to_index(self, file_path: str):
        print(f"Loading PDF: {file_path}")
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks.")

        # Step 3: Index (Embed & Store)
        # This sends text to OpenAI, gets vectors, and stores them in Chroma.
        try:
            self.vector_store.add_documents(chunks)
            print("Documents indexed successfully.")
        except Exception as e:
            error_msg = str(e)
            if "insufficient_quota" in error_msg:
                raise Exception("OpenAI API Quota Exceeded. Please check your billing at platform.openai.com/account/billing")
            raise e

        return len(chunks)

    def query_rag(self, question: str) -> str:
        """
        RETRIEVAL & GENERATION (Modern LCEL Approach)
        """
        # Helper to format documents
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # Prompt
        prompt_template = """Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:"""
        
        custom_prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # LCEL Chain
        # 1. Retrieve docs (retriever) -> Format them
        # 2. Pass question through
        # 3. Send to Prompt -> LLM -> String Output
        rag_chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | custom_prompt
            | self.llm
            | StrOutputParser()
        )

        response = rag_chain.invoke(question)
        return response

# Singleton instance
rag_service = RAGService()
