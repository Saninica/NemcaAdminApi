from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.schemas.language import LanguageCreate, LanguageRead
from src.crud.languages import crud_lang
from src.dependencies import get_current_user, get_db


router = APIRouter()

@router.post("/", response_model=LanguageRead, dependencies=[Depends(get_current_user)])
async def create_lang(lang: LanguageCreate, db: AsyncSession = Depends(get_db)):
    created_lang = await crud_lang.create(db, obj_in=lang)
    return created_lang


@router.get("/{lang_id}", response_model=LanguageRead, dependencies=[Depends(get_current_user)])
async def read_lang(lang_id: int, db: AsyncSession = Depends(get_db)):
    lang = await crud_lang.get(db, id=lang_id)
    if not lang:
        raise HTTPException(status_code=404, detail="Language not found")
    return lang

@router.get("/", response_model=List[LanguageRead], dependencies=[Depends(get_current_user)])
async def read_langs(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    langs = await crud_lang.get_multi(db, skip=skip, limit=limit)
    return langs


@router.delete("/{lang_id}", response_model=dict, dependencies=[Depends(get_current_user)])
async def delete_lang(lang_id: int, db: AsyncSession = Depends(get_db)):
    lang = await crud_lang.remove(db, id=lang_id)
    if not lang:
        raise HTTPException(status_code=404, detail="Language not found")
    return {"detail": "Language deleted successfully"}