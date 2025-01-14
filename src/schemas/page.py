from pydantic import BaseModel
from typing import List, Optional


class PageBase(BaseModel):
    name: str  # e.g., 'home', 'about_us'
    website_id: int

class PageCreate(PageBase):
    pass

class PageRead(PageBase):
    id: int

    class Config:
        from_attributes = True

class PageUpdate(PageBase):
    name: Optional[str] = None
    website_id: Optional[int] = None


class PageContentSchema(BaseModel):
    id: int
    page_id: int
    website_id: int
    language_code: str
    title: str
    body: str
    cover_image: Optional[str]

    class Config:
        from_attributes = True

class PageSchema(BaseModel):
    id: int
    name: str
    contents: Optional[List[PageContentSchema]] = []

    class Config:
        from_attributes = True

class PageContentCreate(BaseModel):
    page_id: int
    website_id: int
    language_code: str
    title: str
    body: str
    cover_image: Optional[str] = None


class PageContentUpdate(BaseModel):
    website_id: int
    language_code: str
    title: str
    body: str
    cover_image: Optional[str]

class PageContentRead(PageContentSchema):
    id: int
    page_id: int

    class Config:
        from_attributes = True

PageCreate.model_rebuild()
PageRead.model_rebuild()