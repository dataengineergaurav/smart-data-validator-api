from pydantic import BaseModel, Field
from typing import List

class ColumnRule(BaseModel):
    name: str = Field(..., description="Column name")
    age: int = Field(..., description="Column age in years")
    salary: float = Field(..., description="Column salary in USD")
    required: bool = True

class ValidationRequest(BaseModel):
    rules: List[ColumnRule]

class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str] = []
