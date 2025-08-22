import pandas as pd
from app.models.schema import ValidationRequest, ValidationResult

def validate_csv(file_path: str, request: ValidationRequest) -> ValidationResult:
    df = pd.read_csv(file_path)
    errors = []

    for rule in request.rules:
        if rule.name not in df.columns:
            errors.append(f"Missing column: {rule.name}")
            continue

        if rule.required and df[rule.name].isnull().any():
            errors.append(f"Null values in required column: {rule.name}")

    return ValidationResult(is_valid=(len(errors) == 0), errors=errors)
