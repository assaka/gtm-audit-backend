from fastapi import APIRouter, UploadFile, Request
from services.audit_processor import analyze_uploaded_file, stream_response

router = APIRouter()

@router.post("/upload-gtm")
async def upload_gtm(file: UploadFile, request: Request):
    user_id = request.headers.get("X-User-ID", "guest")
    session_id = await analyze_uploaded_file(file, user_id)
    return {"session_id": session_id}

@router.get("/stream/{session_id}")
async def stream(session_id: str):
    return stream_response(session_id)
