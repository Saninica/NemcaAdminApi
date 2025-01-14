from pydantic import BaseModel
from datetime import datetime


class Announcement(BaseModel):
    id: int
    title: str
    body: str
    cover_image: str
    start_date: datetime
    end_date: datetime
    created_at: datetime
    page_id: int
    website_id: int
    language_code: str


class AnnouncementCreate(BaseModel):
    title: str
    body: str
    cover_image: str
    start_date: datetime
    end_date: datetime
    page_id: int
    website_id: int
    language_code: str

class AnnouncementUpdate(BaseModel):
    title: str
    body: str
    cover_image: str
    start_date: datetime
    end_date: datetime
    page_id: int
    website_id: int
    language_code: str

class AnnouncementRead(Announcement):
    id: int

    class Config:
        form_attributes = True

    

