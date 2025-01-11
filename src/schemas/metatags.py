from pydantic import BaseModel

class MetatagsBase(BaseModel):
    title: str
    description: str
    keywords: str


class MetatagsCreate(MetatagsBase):
    page_id: int
    website_id: int
    language_code: str


class MetatagsUpdate(MetatagsBase):
    page_id: int
    language_code: str
    website_id: int


class Metatags(MetatagsCreate):
    id: int

    class Config:
        form_attributes = True