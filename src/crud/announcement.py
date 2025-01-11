from .base import CRUDBase
from src.models.announcements import Announcement
from src.schemas.announcement import AnnouncementCreate, AnnouncementUpdate


class CRUDBaseAnnouncement(CRUDBase[Announcement, AnnouncementCreate, AnnouncementUpdate]):
    pass

crud_announcement = CRUDBaseAnnouncement(Announcement)
