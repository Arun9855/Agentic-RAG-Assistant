import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

def ingest_data():
    print("Loading documents from data/...")
    loader = DirectoryLoader('data', glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()
    
    print(f"Loaded {len(documents)} documents.")
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    docs = text_splitter.split_documents(documents)
    print(f"Split into {len(docs)} chunks.")
    
    # Use Local Embeddings (no key needed)
    print("Initializing Local Embeddings (Sentence Transformers)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Create and persist vector store
    # Note: Vector store path is chroma_db
    print("Creating vector store in ./chroma_db...")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    # Ensure persistence
    vectorstore.persist()
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_data()
