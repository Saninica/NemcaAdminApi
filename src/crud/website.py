from .base import CRUDBase
from src.models.website import Website
from src.schemas.website import WebsiteCreate, WebsiteUpdate
from fastapi import UploadFile


class CRUDWebsite(CRUDBase[Website, WebsiteCreate, WebsiteUpdate]):
    async def upload_favicon(self, favicon: UploadFile):
        favicon_path = f"media/website/{favicon.filename}"

        with open(favicon_path, "wb+") as f:
            f.write(await favicon.read())

        return favicon_path

crud_website = CRUDWebsite(Website)
