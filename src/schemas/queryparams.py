from pydantic import BaseModel
from typing import Optional

class PageContentQueryParams(BaseModel):
    skip: int = 0
    limit: int = 100
    website_id: Optional[int] = None
    page_id: Optional[int] = None
    language_code: Optional[str] = None


class LanguageQueryParams(BaseModel):
    skip: int = 0
    limit: int = 100
    website: Optional[int] = None
    lang: Optional[str] = None


class LanguageUpdateParams(BaseModel):
    lang: Optional[str] = None  
    website: Optional[int] = None