from fastapi import APIRouter, UploadFile, File, Form
from app.services.dify_connector import call_dify
from app.services.validator import validate_csv
from app.models.schema import ValidationRequest
import json

router = APIRouter()

@router.post("/validate")
async def validate_file(
    file: UploadFile = File(...),
    request: str = Form(...)
):
    # local dev
    # try:
    #     request_obj = ValidationRequest(**json.loads(request))
    # except Exception as e:
    #     return {"error": "Invalid JSON in 'request' field", "detail": str(e)}
    
    # production
    with open(file.filename, "wb") as f:
        f.write(await file.read())
    result = validate_csv(file.filename, request_obj)
    ai_suggestions = None
    if not result.is_valid:
        error_summary = "\n".join(result.errors)
        query = f"The CSV failed validation. Errors:\n{error_summary}\nSuggest fixes."
        ai_suggestions = call_dify(query)

    return {
        "validation": result.model_dump(),
        "ai_suggestions": ai_suggestions,
    }

@router.get("/health")
async def health_check():
    return {"status": "ok"}