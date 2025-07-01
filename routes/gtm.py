from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from services.audit_processor import analyze_uploaded_file, stream_response, process_audit
from models.audit_schema import AuditRequestSchema, AuditResponseSchema

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


@router.post("/gtm/audit", response_model=AuditResponseSchema)
async def audit_gtm(request: AuditRequestSchema):
    result = process_audit(request.url)
    return AuditResponseSchema(
        id="sample-id",  # You can replace this with real ID logic
        timestamp="2025-07-01T00:00:00Z",  # Replace with real timestamp
        url=request.url,
        audit_summary=result["summary"]  # Make sure 'summary' key exists in result
    )


