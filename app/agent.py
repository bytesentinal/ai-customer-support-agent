from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.config import GROQ_API_KEY, MODEL_NAME, CHROMA_DIR

chat_history = []

def build_agent():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME, temperature=0.3)
    return retriever, llm

def ask(retriever, llm, question: str) -> str:
    docs = retriever.invoke(question)
    context = "\n".join([doc.page_content for doc in docs])
    history_text = "\n".join([f"User: {h['user']}\nAssistant: {h['assistant']}" for h in chat_history])

    prompt = f"""You are a helpful customer support agent.
Answer using ONLY the context below. If the answer isn't there, say "I don't have that information — please contact us directly."

Context:
{context}

Chat History:
{history_text}

Question: {question}
Answer:"""

    response = llm.invoke(prompt)
    answer = response.content
    chat_history.append({"user": question, "assistant": answer})
    return answer

def reset_memory():
    global chat_history
    chat_history = []