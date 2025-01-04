from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.crud.base import CRUDBase
from src.models.languages import Language
from src.schemas.language import LanguageCreate


class CRUDLanguage(CRUDBase[Language, LanguageCreate, None]):
    pass


crud_lang = CRUDLanguage(Language)