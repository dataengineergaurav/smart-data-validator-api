from pydantic import BaseModel, Field
from typing import List, Literal

class ColumnRule(BaseModel):
    name: str = Field(..., description="Column name")
    dtype: Literal["string", "int", "float"] = Field(..., description="Expected data type")
    required: bool = Field(default=True, description="Whether column is mandatory")

class ValidationRequest(BaseModel):
    rules: List[ColumnRule]

class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str] = []
