from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/analyze")
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        # You can call your processing logic here
        # For now, just return file name to test it
        return JSONResponse(content={"filename": file.filename, "status": "received"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


