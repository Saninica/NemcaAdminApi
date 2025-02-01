from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy.future import select
from src.models import Language, User
from src.schemas.language import LanguageCreate, LanguageRead, LanguageUpdate, PaginatedLanguageResponse
from src.crud.languages import crud_lang
from src.dependencies import get_current_user, get_db
from src.schemas.queryparams import LanguageQueryParams, LanguageUpdateParams


router = APIRouter()

@router.post("/", response_model=LanguageRead)
async def create_lang(lang: LanguageCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        lang.website_id = current_user.websites[0].id
        
    created_lang = await crud_lang.create(db, obj_in=lang)
    return created_lang


@router.get("/{lang_id}", response_model=LanguageRead)
async def read_lang(lang_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        lang = await crud_lang.get(db, id=lang_id, filters={"website_id": current_user.websites[0].id})
    else:
        lang = await crud_lang.get(db, id=lang_id)
        
    if not lang:
        raise HTTPException(status_code=404, detail="Language not found")
    return lang

@router.get("/", response_model=PaginatedLanguageResponse)
async def read_langs(query: LanguageQueryParams = Depends(), db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    langs = []

    if query.lang:
        if current_user.is_superuser is False:
            langs = await crud_lang.get_filtered(db, filters={"code": query.lang, "website_id": current_user.websites[0].id}, skip=query.skip, limit=query.limit)
        else:
            langs = await crud_lang.get_filtered(db, filters={"code": query.lang}, skip=query.skip, limit=query.limit)
    else:
        if current_user.is_superuser is False:
            langs = await crud_lang.get_multi(db, skip=query.skip, limit=query.limit, filters={"website_id": current_user.websites[0].id})
        else:
            langs = await crud_lang.get_multi(db, skip=query.skip, limit=query.limit)

    total_stmt = select(func.count()).select_from(Language)
    total_result = await db.execute(total_stmt)
    total = total_result.scalar_one()

    return PaginatedLanguageResponse(
        items=langs,
        total=total,
        limit=query.limit,
        skip=query.skip
    )


@router.delete("/{lang_id}", response_model=dict)
async def delete_lang(lang_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        lang = await crud_lang.remove(db, id=lang_id, filters={"website_id": current_user.websites[0].id})
    else:
        lang = await crud_lang.remove(db, id=lang_id)
    
    if not lang:
        raise HTTPException(status_code=404, detail="Language not found")
    return {"detail": "Language deleted successfully"}


@router.put("/", response_model=LanguageRead)
async def update_lang(lang: LanguageUpdate, query: LanguageUpdateParams = Depends(), db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        db_lang = await crud_lang.get(db, id=None, filters={"code": query.lang, "website_id": current_user.websites[0].id})
    else:
        db_lang = await crud_lang.get(db, id=None, filters={"code": query.lang})
    
    if not db_lang:
        raise HTTPException(status_code=404, detail="Language not found")

    updated_lang = await crud_lang.update(db, db_obj=db_lang, obj_in=lang)
    return updated_lang