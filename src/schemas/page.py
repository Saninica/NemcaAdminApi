from pydantic import BaseModel
from typing import List, Optional


class PageBase(BaseModel):
    name: str  # e.g., 'home', 'about_us'

class PageCreate(PageBase):
    pass

class PageRead(PageBase):
    id: int

    class Config:
        from_attributes = True


class PageContentSchema(BaseModel):
    id: int
    page_id: int
    language_code: str
    title: str
    body: str

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
    language_code: str
    title: str
    body: str

class PageUpdate(PageBase):
    name: Optional[str] = None

class PageContentUpdate(PageContentSchema):
    pass

class PageContentRead(PageContentSchema):
    id: int
    page_id: int

    class Config:
        from_attributes = True

PageCreate.update_forward_refs()
PageRead.update_forward_refs()