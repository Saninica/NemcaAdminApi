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

    async def get_multiple_contents(self, db: AsyncSession, page_id: int, website_id: int, language_code: str):
        stmt = (
        select(self.model)
        .options(joinedload(PageContent.page))  # Load the related Page model
        .where(
            self.model.page_id == page_id,
            self.model.website_id == website_id,
            self.model.language_code == language_code
        ))
        result = await db.execute(stmt)
        return result.scalars()

crud_page_content = CRUDPageContents(PageContent)