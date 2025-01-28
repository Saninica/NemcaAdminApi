from pydantic import BaseModel
from typing import Optional

class MetatagsBase(BaseModel):
    title: str
    description: str
    keywords: str


class MetatagsCreate(MetatagsBase):
    page_id: int
    website_id: Optional[int] = None
    language_id: int


class MetatagsUpdate(MetatagsBase):
    page_id: int
    language_id: int
    website_id: int


class Metatags(MetatagsCreate):
    id: int

    class Config:
        form_attributes = True