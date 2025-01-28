from pydantic import BaseModel
from typing import Optional

class LanguageBase(BaseModel):
    code: str  # e.g., 'en', 'tr'
    name: str  # e.g., 'English', 'Turkish'
    website_id: Optional[int] = None

class LanguageCreate(LanguageBase):
    pass

class LanguageUpdate(LanguageBase):
    pass

class LanguageRead(LanguageBase):
    id: int

    class Config:
        from_attributes = True