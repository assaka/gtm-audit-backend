import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Available Gemini models:")
for m in genai.list_models():  # iterate directly
    print(" -", m.name)

