from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from collections import defaultdict

from src.crud.base import CRUDBase
from src.models.pages import Page, PageContent
from src.schemas.page import PageCreate, PageUpdate


class CRUDPage(CRUDBase[Page, PageCreate, PageUpdate]):
    async def get_with_contents(self, db: AsyncSession, id: int) -> Optional[Page]:
        """
        Retrieve a Page by its ID and attach its related PageContent instances.
        """
        # Fetch the Page
        page = await db.get(Page, id)
        if not page:
            return None

        # Fetch related PageContent instances
        result = await db.execute(
            select(PageContent).where(PageContent.page_id == id)
        )
        contents = result.scalars().all()

        # Dynamically attach contents to the Page object
        setattr(page, 'contents', contents)

        return page

    async def get_multi_with_contents(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Page]:
        """
        Retrieve multiple Pages and attach their related PageContent instances.
        """
        # Fetch Pages with pagination
        result = await db.execute(
            select(Page).offset(skip).limit(limit)
        )
        pages = result.scalars().all()
        if not pages:
            return pages

        # Extract Page IDs
        page_ids = [page.id for page in pages]

        # Fetch all related PageContent instances in bulk
        contents_result = await db.execute(
            select(PageContent).where(PageContent.page_id.in_(page_ids))
        )
        contents = contents_result.scalars().all()

        # Organize contents by page_id for efficient attachment
        contents_by_page = defaultdict(list)
        for content in contents:
            contents_by_page[content.page_id].append(content)

        # Attach contents to each Page object
        for page in pages:
            setattr(page, 'contents', contents_by_page.get(page.id, []))

        return pages

# Instantiate CRUDPage
crud_page = CRUDPage(Page)