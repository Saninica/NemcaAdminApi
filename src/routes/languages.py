from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.models import User
from src.schemas.language import LanguageCreate, LanguageRead, LanguageUpdate
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

@router.get("/", response_model=List[LanguageRead])
async def read_langs(query: LanguageQueryParams = Depends(), db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    langs = []

    if query.lang:
        if current_user.is_superuser is False:
            langs = await crud_lang.get_filtered(db, filters={"code": query.lang, "website_id": current_user.websites[0].id})
        else:
            langs = await crud_lang.get_filtered(db, filters={"code": query.lang})
    else:
        if current_user.is_superuser is False:
            langs = await crud_lang.get_multi(db, skip=query.skip, limit=query.limit, filters={"website_id": current_user.websites[0].id})
        else:
            langs = await crud_lang.get_multi(db, skip=query.skip, limit=query.limit)

    return langs


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