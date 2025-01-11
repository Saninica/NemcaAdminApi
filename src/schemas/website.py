from pydantic import BaseModel
from typing import Optional


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