from pydantic import BaseModel

class LanguageBase(BaseModel):
    code: str  # e.g., 'en', 'tr'
    name: str  # e.g., 'English', 'Turkish'

class LanguageCreate(LanguageBase):
    pass

class LanguageRead(LanguageBase):
    class Config:
        from_attributes = True