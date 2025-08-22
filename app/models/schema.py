from pydantic import BaseModel, Field
from typing import List

class ColumnRule(BaseModel):
    name: str = Field(..., description="Column name")
    dtype: str = Field(..., description="Expected data type")
    required: bool = True

class ValidationRequest(BaseModel):
    rules: List[ColumnRule]

class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str] = []
