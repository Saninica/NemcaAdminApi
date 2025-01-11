from pydantic import BaseModel


class Announcement(BaseModel):
    title: str
    content: str
    cover_image: str


class AnnouncementCreate(Announcement):
    pass

class AnnouncementUpdate(Announcement):
    pass

class AnnouncementRead(Announcement):
    id: int

    class Config:
        form_attributes = True

    

