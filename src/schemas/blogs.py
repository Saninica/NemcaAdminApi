from pydantic import BaseModel
from typing import Optional

class BlogBase(BaseModel):
    website_id: Optional[int] = None
    page_id: Optional[int] = None
    language_code: Optional[str] = None
    body: str


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BlogBase):
    pass

class BlogRead(BlogBase):
    id: int

    class Config:
        form_attributes = True