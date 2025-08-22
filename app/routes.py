from fastapi import APIRouter, UploadFile
from app.services.validator import validate_csv
from app.models.schema import ValidationRequest

router = APIRouter()

@router.post("/validate")
async def validate_file(file: UploadFile, request: ValidationRequest):
    with open(file.filename, "wb") as f:
        f.write(await file.read())
    result = validate_csv(file.filename, request)
    return result.model_dump()
