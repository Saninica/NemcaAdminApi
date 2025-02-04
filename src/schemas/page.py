from pydantic import BaseModel
from typing import List, Optional


class PageBase(BaseModel):
    name: str  # e.g., 'home', 'about_us'
    website_id: Optional[int] = 0

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
    website_id: Optional[int] = None
    language_id: int
    title: str
    body: str
    price: Optional[float] = None
    cover_image: Optional[str] = None


class PageContentUpdate(BaseModel):
    page_id: int
    website_id: int
    language_id: int
    title: str
    body: str
    price: Optional[float] = None
    cover_image: Optional[str]

class PageContentRead(BaseModel):
    id: int
    page_id: int
    website_id: int
    language_id: int
    title: str
    body: str
    price: Optional[float] = None
    cover_image: Optional[str]

    class Config:
        from_attributes = True

class PageContentMultiple(BaseModel):
    id: int
    page: str
    website: str
    language_code: str
    title: str
    body: str
    price:  Optional[float] = None
    cover_image: Optional[str]

    class Config:
        from_attributes = True

class PaginatedPageContentResponse(BaseModel):
    items: List[PageContentMultiple]
    total: int  # total number of items in DB
    limit: int
    skip: int

PageCreate.model_rebuild()
PageRead.model_rebuild()