from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.crud.base import CRUDBase
from src.models.pages import PageContent
from src.schemas.page import PageContentCreate, PageContentUpdate


class CRUDPageContents(CRUDBase[PageContent, PageContentCreate, PageContentUpdate]):
    pass

crud_page_content = CRUDPageContents(PageContent)