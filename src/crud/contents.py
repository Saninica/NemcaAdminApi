from src.crud.base import CRUDBase
from src.models.pages import PageContent
from src.schemas.page import PageContentCreate, PageContentUpdate
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload


class CRUDPageContents(CRUDBase[PageContent, PageContentCreate, PageContentUpdate]):
    async def upload_cover_image(self, cover_image: UploadFile):
        cover_image_path = f"media/content/{cover_image.filename}"

        with open(cover_image_path, "wb+") as f:
            f.write(await cover_image.read())

        return cover_image_path


crud_page_content = CRUDPageContents(PageContent)