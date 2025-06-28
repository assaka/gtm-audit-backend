from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from services.audit_processor import analyze_uploaded_file, stream_response
from urllib.parse import unquote
import os, json

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile = File(...), user_id: str = Form(...)):
    try:
        session_id = await analyze_uploaded_file(file, user_id)
        return {"session_id": session_id}
    except Exception as e:
        print("❌ Analyze Error:", str(e))  # 👈 Debug print
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/stream/{session_id}")
async def stream(session_id: str):
    return stream_response(session_id)

@router.get("/history/{user_id}")
def get_history(user_id: str):
    path = f"history/{user_id}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

@router.delete("/delete/{user_id}/{timestamp}")
def delete_entry(user_id: str, timestamp: str):
    path = f"history/{user_id}.json"
    if not os.path.exists(path):
        return JSONResponse(status_code=404, content={"error": "User not found"})

    decoded_ts = unquote(timestamp).replace("Z", "").strip()
    with open(path, "r") as f:
        history = json.load(f)

    filtered = [entry for entry in history if entry["timestamp"].replace("Z", "").strip() != decoded_ts]

    if len(filtered) == len(history):
        return JSONResponse(status_code=404, content={"error": "Entry not found"})

    with open(path, "w") as f:
        json.dump(filtered, f, indent=2)

    return {"status": "deleted"}


