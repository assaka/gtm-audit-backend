from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from gemini_embedding import GeminiEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# Load ChromaDB
persist_directory = "chroma_db"
embedding = GeminiEmbeddings(api_key=os.getenv("GEMINI_API_KEY"))
vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# Take user query
query = input("🔎 Ask your GTM question: ")

# Search top 3 relevant chunks
results = vectorstore.similarity_search(query, k=3)

print("\n📌 Top Matches:")
for i, doc in enumerate(results, 1):
    print(f"\nResult {i}:")
    print(doc.page_content[:500])  # Print first 500 chars
    print(f"\n🔗 Source: {doc.metadata.get('source')}")
