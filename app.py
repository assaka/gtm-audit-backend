# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from routers import audit



# app= FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # frontend origin
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Backend is running!"}
# app.include_router(audit.router)




# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from routers import audit  # assuming this is your custom router module

# app = FastAPI()

# # Add CORS middleware to support frontend calls from localhost:3000
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def read_root():
#     return {"message": "Backend is running!"}

# # Include additional routes from routers/audit.py
# app.include_router(audit.router)


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust as needed
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     # handle file logic
#     return {"parsed_data": parsed_data}


# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # CORS setup
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.post("/test-parse")
# async def test_parse(file: UploadFile = File(...)):
#     content = await file.read()
    
#     # Simulate parsing logic — replace with your real logic
#     filename = file.filename
#     size = len(content)

#     return {
#         "filename": filename,
#         "size": size,
#         "message": "File received successfully!"
#     }


# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# import zipfile
# import tempfile
# import json
# import os

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.post("/test-parse")
# async def test_parse(file: UploadFile = File(...)):
#     try:
#         # Save uploaded file to a temporary location
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
#             tmp_zip.write(await file.read())
#             tmp_zip_path = tmp_zip.name

#         # Unzip and look for data.json
#         with zipfile.ZipFile(tmp_zip_path, "r") as zip_ref:
#             zip_ref.extractall(tempfile.gettempdir())
#             extracted_files = zip_ref.namelist()

#         # Look for a JSON file in the extracted contents
#         data_json_path = None
#         for fname in extracted_files:
#             if fname.endswith(".json"):
#                 data_json_path = os.path.join(tempfile.gettempdir(), fname)
#                 break

#         if not data_json_path or not os.path.exists(data_json_path):
#             return {"error": "No JSON file found in uploaded zip."}

#         # Read and parse JSON content
#         with open(data_json_path, "r") as f:
#             parsed_data = json.load(f)

#         # Return dummy audit summary for now
#         return {
#             "status": "success",
#             "file": file.filename,
#             "extracted_json_keys": list(parsed_data.keys()),
#             "example_data": parsed_data,
#             "message": "Audit parsed successfully!",
#         }

#     except Exception as e:
#         return {"error": str(e)}


# import google.generativeai as genai
# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware

# from dotenv import load_dotenv
# import os, json, zipfile, io

# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app = FastAPI()

# @app.post("/analyze")
# async def analyze_file(file: UploadFile = File(...)):
#     contents = await file.read()
#     with zipfile.ZipFile(io.BytesIO(contents)) as z:
#         for name in z.namelist():
#             if name.endswith(".json"):
#                 data = json.loads(z.read(name))
#                 break

#     input_json = json.dumps(data.get("containerVersion", {}), indent=2)
#     model = genai.GenerativeModel("gemini-2.0-flash-exp")
#     response = model.generate_content(
#         f"You are a GTM auditor. Analyze this GTM container:\n{input_json}"
#     )
#     print(response)
#     return {"status": "success", "audit_summary": response.text}






# import google.generativeai as genai
# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# import os, json, zipfile, io
# from dotenv import load_dotenv

# # Load environment
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Create app
# app = FastAPI()

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.post("/analyze")
# async def analyze_file(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         with zipfile.ZipFile(io.BytesIO(contents)) as z:
#             for name in z.namelist():
#                 if name.endswith(".json"):
#                     data = json.loads(z.read(name))
#                     break
#             else:
#                 return JSONResponse(content={"error": "No JSON file found in ZIP."}, status_code=400)

#         input_json = json.dumps(data.get("containerVersion", {}), indent=2)
#         model = genai.GenerativeModel("gemini-2.0-flash-exp")
#         response = model.generate_content(
#             f"You are a GTM auditor. Analyze this GTM container:\n{input_json}"
#         )

#         return {"status": "success", "audit_summary": response.text}
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)

# @app.post("/analyze")
# async def analyze_file(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         with zipfile.ZipFile(io.BytesIO(contents)) as z:
#             for name in z.namelist():
#                 if name.endswith(".json"):
#                     data = json.loads(z.read(name))
#                     break
#             else:
#                 return JSONResponse(content={"error": "No JSON file found in ZIP."}, status_code=400)

#         input_json = json.dumps(data.get("containerVersion", {}), indent=2)
#         model = genai.GenerativeModel("gemini-2.0-flash-exp")
#         response = model.generate_content(
#             f"You are a GTM auditor. Analyze this GTM container:\n{input_json}"
#         )

#         return {"result": response.text}
    
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return JSONResponse(status_code=500, content={"error": str(e)})





# import google.generativeai as genai
# from fastapi import FastAPI, File, UploadFile, Form
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
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





import google.generativeai as genai
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from urllib.parse import unquote
import os, json, zipfile, io
from dotenv import load_dotenv
from datetime import datetime

# Load environment
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create FastAPI app
app = FastAPI()

# Enable CORS for all origins (for local frontend dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure history folder exists
HISTORY_DIR = "history"
os.makedirs(HISTORY_DIR, exist_ok=True)


@app.post("/analyze")
async def analyze_file(
    file: UploadFile = File(...),
    user_id: str = Form(...)
):
    try:
        contents = await file.read()
        with zipfile.ZipFile(io.BytesIO(contents)) as z:
            for name in z.namelist():
                if name.endswith(".json"):
                    data = json.loads(z.read(name))
                    break
            else:
                return JSONResponse(content={"error": "No JSON file found in ZIP."}, status_code=400)

        # Prepare input and analyze with Gemini
        input_json = json.dumps(data.get("containerVersion", {}), indent=2)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(
            f"You are a GTM auditor. Analyze this GTM container:\n{input_json}"
        )
        audit_result = response.text

        # Build audit record
        record = {
            "filename": file.filename,
            "result": audit_result,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        # Save to user's history
        history_path = os.path.join(HISTORY_DIR, f"{user_id}.json")
        if os.path.exists(history_path):
            with open(history_path, "r") as f:
                history = json.load(f)
        else:
            history = []

        history.append(record)

        with open(history_path, "w") as f:
            json.dump(history, f, indent=2)

        return {"result": audit_result}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/history/{user_id}")
def get_audit_history(user_id: str):
    history_path = os.path.join(HISTORY_DIR, f"{user_id}.json")
    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            return json.load(f)
    else:
        return []  # Return empty array instead of 404


@app.delete("/delete/{user_id}/{timestamp}")
def delete_audit_entry(user_id: str, timestamp: str):
    history_path = os.path.join(HISTORY_DIR, f"{user_id}.json")
    if not os.path.exists(history_path):
        return JSONResponse(status_code=404, content={"error": "User not found"})

    decoded_ts = unquote(timestamp)

    def normalize(ts: str) -> str:
        return ts.replace("Z", "").strip()

    decoded_ts = normalize(decoded_ts)

    with open(history_path, "r") as f:
        history = json.load(f)

    original_len = len(history)
    history = [entry for entry in history if normalize(entry["timestamp"]) != decoded_ts]

    if len(history) == original_len:
        return JSONResponse(status_code=404, content={"error": "Entry not found"})

    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

    return {"status": "deleted"}

