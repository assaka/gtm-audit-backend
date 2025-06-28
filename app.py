# from routers import audit
# import google.generativeai as genai
# from fastapi import FastAPI, File, UploadFile, Form
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from urllib.parse import unquote
# import os, json, zipfile, io
# from dotenv import load_dotenv
# from datetime import datetime

# # Load environment
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Create FastAPI app
# app = FastAPI()

# # Enable CORS for all origins (for local frontend dev)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Ensure history folder exists
# HISTORY_DIR = "history"
# os.makedirs(HISTORY_DIR, exist_ok=True)


# @app.post("/analyze")
# async def analyze_file(
#     file: UploadFile = File(...),
#     user_id: str = Form(...)
# ):
#     try:
#         contents = await file.read()
#         with zipfile.ZipFile(io.BytesIO(contents)) as z:
#             for name in z.namelist():
#                 if name.endswith(".json"):
#                     data = json.loads(z.read(name))
#                     break
#             else:
#                 return JSONResponse(content={"error": "No JSON file found in ZIP."}, status_code=400)

#         # Prepare input and analyze with Gemini
#         input_json = json.dumps(data.get("containerVersion", {}), indent=2)
#         model = genai.GenerativeModel("gemini-2.0-flash-exp")
#         response = model.generate_content(
#             f"You are a GTM auditor. Analyze this GTM container:\n{input_json}"
#         )
#         audit_result = response.text

#         # Build audit record
#         record = {
#             "filename": file.filename,
#             "result": audit_result,
#             "timestamp": datetime.utcnow().isoformat() + "Z"
#         }

#         # Save to user's history
#         history_path = os.path.join(HISTORY_DIR, f"{user_id}.json")
#         if os.path.exists(history_path):
#             with open(history_path, "r") as f:
#                 history = json.load(f)
#         else:
#             history = []

#         history.append(record)

#         with open(history_path, "w") as f:
#             json.dump(history, f, indent=2)

#         return {"result": audit_result}

#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return JSONResponse(status_code=500, content={"error": str(e)})


# @app.get("/history/{user_id}")
# def get_audit_history(user_id: str):
#     history_path = os.path.join(HISTORY_DIR, f"{user_id}.json")
#     if os.path.exists(history_path):
#         with open(history_path, "r") as f:
#             return json.load(f)
#     else:
#         return []  # Return empty array instead of 404


# @app.delete("/delete/{user_id}/{timestamp}")
# def delete_audit_entry(user_id: str, timestamp: str):
#     history_path = os.path.join(HISTORY_DIR, f"{user_id}.json")
#     if not os.path.exists(history_path):
#         return JSONResponse(status_code=404, content={"error": "User not found"})

#     decoded_ts = unquote(timestamp)

#     def normalize(ts: str) -> str:
#         return ts.replace("Z", "").strip()

#     decoded_ts = normalize(decoded_ts)

#     with open(history_path, "r") as f:
#         history = json.load(f)

#     original_len = len(history)
#     history = [entry for entry in history if normalize(entry["timestamp"]) != decoded_ts]

#     if len(history) == original_len:
#         return JSONResponse(status_code=404, content={"error": "Entry not found"})

#     with open(history_path, "w") as f:
#         json.dump(history, f, indent=2)

#     return {"status": "deleted"}



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import audit
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("history", exist_ok=True)

app.include_router(audit.router)

