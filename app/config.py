from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"
CHROMA_DIR = "./chroma_db"     # where ChromaDB stores its data
DOCS_DIR = "./docs"            # where client documents go