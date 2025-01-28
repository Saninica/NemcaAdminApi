from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Announcement(BaseModel):
    id: int
    title: str
    body: str
    cover_image: str
    start_date: datetime
    end_date: datetime
    created_at: Optional[datetime] = None
    page_id: int
    website_id: int
    language_id: int


class AnnouncementCreate(BaseModel):
    title: str
    body: str
    cover_image: str
    start_date: datetime
    end_date: datetime
    page_id: int
    website_id: Optional[int] = None
    language_id: int

class AnnouncementUpdate(BaseModel):
    title: str
    body: str
    cover_image: str
    start_date: datetime
    end_date: datetime
    page_id: int
    website_id: Optional[int] = None
    language_id: int

class AnnouncementRead(Announcement):
    id: int

    class Config:
        form_attributes = True

    

