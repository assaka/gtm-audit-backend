# file: utils/embed_articles.py
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
import os
# from langchain_community.embeddings import OpenAIEmbeddings
from gemini_embedding import GeminiEmbeddings

from dotenv import load_dotenv
load_dotenv() 

API_KEY = os.getenv("GEMINI_API_KEY")


# Step 1: Load saved articles
with open("gtm_articles.json", "r", encoding="utf-8") as f:
    raw_articles = json.load(f)

print(f"🔍 Loaded {len(raw_articles)} articles")

# Step 2: Convert to LangChain Documents
docs = []
for article in raw_articles:
    doc = Document(
        page_content=article["content"],
        metadata={"source": article["url"]}
    )
    docs.append(doc)

# Step 3: Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(docs)
print(f"📄 Total chunks: {len(chunks)}")

# Step 4: Embed and store in ChromaDB
persist_directory = "chroma_db"
os.makedirs(persist_directory, exist_ok=True)

embedding = GeminiEmbeddings(api_key=os.getenv("GEMINI_API_KEY"))
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory=persist_directory
)

print(f"✅ Embeddings stored in ChromaDB: {persist_directory}")
