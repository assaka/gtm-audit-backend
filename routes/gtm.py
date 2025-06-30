from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from services.audit_processor import analyze_uploaded_file, stream_response, process_audit

router = APIRouter()

@router.post("/gtm/upload")
async def upload_gtm_file(file: UploadFile, user_id: str):
    try:
        session_id = await analyze_uploaded_file(file, user_id)
        return {"session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/gtm/stream/{session_id}")
async def stream_gtm_results(session_id: str):
    return stream_response(session_id)


@router.get("/gtm/simple-audit")
def simple_audit(url: str):
    result = process_audit(url)
    return JSONResponse(content=result)


