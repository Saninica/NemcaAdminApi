from pydantic import BaseModel
from typing import List, Dict, Optional


class ForeignKeyInfo(BaseModel):
    target_table: str
    target_model: str
    target_field: str

class FieldMetadata(BaseModel):
    type: str
    nullable: bool
    primary_key: bool
    foreign_key: Optional[ForeignKeyInfo] = None

class ModelMetadata(BaseModel):
    models: Dict[str, Dict[str, FieldMetadata]]

