"""
ingest.py — RAG Pipeline

What this does, step by step:
1. Load documents from the /docs folder (PDF or TXT)
2. Split them into smaller chunks (so the LLM doesn't get overwhelmed)
3. Convert each chunk into a vector (a list of numbers that represents meaning)
4. Store all vectors in ChromaDB (a local vector database)

Run this once per client before starting the agent.
"""

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.config import CHROMA_DIR, DOCS_DIR
import os


def load_documents():
    """Load all PDFs and TXT files from the docs/ folder."""
    documents = []

    for filename in os.listdir(DOCS_DIR):
        filepath = os.path.join(DOCS_DIR, filename)

        if filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
        elif filename.endswith(".txt"):
            loader = TextLoader(filepath, encoding="utf-8")
        else:
            continue  # skip unsupported file types

        documents.extend(loader.load())
        print(f"Loaded: {filename}")

    return documents


def split_documents(documents):
    """
    Split documents into chunks.
    chunk_size=500 means each chunk is ~500 characters.
    chunk_overlap=50 means chunks share 50 chars at edges (so context isn't lost at splits).
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks


def get_embedding_model():
    """
    HuggingFace's all-MiniLM-L6-v2 — free, runs locally, no API key needed.
    It converts text into vectors so we can do similarity search.
    """
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def ingest():
    """Full pipeline: load → split → embed → store."""
    print("Starting ingestion...")

    documents = load_documents()
    if not documents:
        print("No documents found in /docs folder.")
        return

    chunks = split_documents(documents)
    embeddings = get_embedding_model()

    # Store in ChromaDB — creates ./chroma_db folder automatically
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    print(f"Done. {len(chunks)} chunks stored in ChromaDB.")


if __name__ == "__main__":
    ingest()