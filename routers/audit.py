# from fastapi import APIRouter, UploadFile, File
# from utils.file_parser import extract_json_files
# from schema.json_schema import ParsedJSON
# from typing import List
# import zipfile
# router = APIRouter()

# @router.post("/test-parse")
# async def parse_zip_file(file: UploadFile = File(...)):
#     contents = await file.read()
#     parsed_data = extract_json_files(contents)

#     print("🔍 Extracted parsed_data:", parsed_data) 

#     validated_data: List[ParsedJSON] = []
#     for item in parsed_data:
#         try:
#             validated = ParsedJSON(**item)
#             validated_data.append(validated)
#         except Exception as e:
#             continue  # skip invalid items

#     return {"parsed_data": [data.dict() for data in validated_data]}


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


