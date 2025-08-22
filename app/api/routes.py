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
    # local dev without JSON schema validation
    # Uncomment the following lines if you want to validate the request JSON
    # try:
    #     request_obj = ValidationRequest(**json.loads(request))
    # except Exception as e:
    #     return {"error": "Invalid JSON in 'request' field", "detail": str(e)}
    

    with open(file.filename, "wb") as f:
        f.write(await file.read())
    result = validate_csv(file.filename, request_obj)

    # If invalid, call Dify workflow
    ai_suggestions = None
    if not result.is_valid:
        error_summary = "\n".join(result.errors)
        ai_suggestions = call_dify(error_summary)

    return {
        "validation": result.model_dump(),
        "ai_suggestions": ai_suggestions.get("result") if ai_suggestions else None,
    }

@router.get("/health")
async def health_check():
    return {"status": "ok"}