from .base import CRUDBase
from src.models.announcements import Announcement
from src.schemas.announcement import AnnouncementCreate, AnnouncementUpdate
from fastapi import UploadFile, File


class CRUDBaseAnnouncement(CRUDBase[Announcement, AnnouncementCreate, AnnouncementUpdate]):
    async def upload_cover_image(self, cover_image: UploadFile):
        cover_image_path = f"media/announcement/{cover_image.filename}"

        with open(cover_image_path, "wb+") as f:
            f.write(await cover_image.read())

        return cover_image_path

crud_announcement = CRUDBaseAnnouncement(Announcement)
