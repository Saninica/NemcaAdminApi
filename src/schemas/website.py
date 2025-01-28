from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class WebsiteBase(BaseModel):
    name: str
    domain_url: str
    favicon_image: Optional[str] = None


class WebsiteCreate(WebsiteBase):
    pass

class WebsiteUpdate(WebsiteBase):
    pass


class WebsiteRead(WebsiteBase):
    id: int

class WebsiteSchema(BaseModel):
    id: int
    name: str



class PageSchema(BaseModel):
    id: int
    name: str
    website_id: int

    class Config:
        from_attributes = True  # Enable ORM mode (formerly `orm_mode = True`)

# PageContent Schema
class PageContentSchema(BaseModel):
    id: int
    page: str
    website: str
    title: str
    body: str
    cover_image: Optional[str] = None

    class Config:
        from_attributes = True

# Language Schema
class LanguageSchema(BaseModel):
    code: str
    name: str

    class Config:
        from_attributes = True

# Website Schema
class WebsiteSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# Announcement Schema
class AnnouncementSchema(BaseModel):
    id: int
    title: str
    body: str
    cover_image: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    page_id: int
    website_id: int

    class Config:
        from_attributes = True

# MetaTag Schema
class MetaTagSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    keywords: Optional[str] = None
    page_id: int
    website_id: int

    class Config:
        from_attributes = True

# Blog Schema
class BlogSchema(BaseModel):
    id: int
    website_id: int
    page_id: int
    body: str

    class Config:
        from_attributes = True

class ResponseSchema(BaseModel):
    page: Optional[List[PageSchema]]
    contents: Optional[List[PageContentSchema]]
    languages: Optional[List[LanguageSchema]]
    websites: Optional[List[WebsiteBase]]
    announcements: Optional[List[AnnouncementSchema]]
    metatags: Optional[List[MetaTagSchema]]
    blogs: Optional[List[BlogSchema]]

    class Config:
        from_attributes = True