from langchain_community.vectorstores import Chroma
from gemini_embedding import GeminiEmbeddings
from langchain.docstore.document import Document
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize ChromaDB
persist_directory = "chroma_db"
embedding = GeminiEmbeddings(api_key=os.getenv("GEMINI_API_KEY"))
vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# Initialize Gemini Pro
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.0-flash-exp")

# Ask the user a question
query = input("❓ Ask your GTM question: ")

# Retrieve relevant chunks
docs = vectorstore.similarity_search(query, k=4)
context = "\n\n".join([d.page_content for d in docs])

# Generate Gemini answer
prompt = f"""You are an expert on Google Tag Manager. 
Answer the question based only on the context provided below.

Context:
{context}

Question:
{query}

Answer:"""

response = model.generate_content(prompt)
print("\n💬 Gemini Answer:\n")
print(response.text.strip())
