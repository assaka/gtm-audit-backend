# utils/gemini_embedding.py
from langchain_core.embeddings import Embeddings
import google.generativeai as genai

class GeminiEmbeddings(Embeddings):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)

    def embed_documents(self, texts):
        return [
            genai.embed_content(
                model="models/embedding-001",
                content=t,
                task_type="retrieval_document"
            )["embedding"]
            for t in texts
        ]

    def embed_query(self, text):
        return genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_query"
        )["embedding"]
