from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.schemas.page import PageCreate, PageRead, PageUpdate
from src.crud.pages import crud_page
from src.dependencies import get_current_user, get_db


router = APIRouter()

@router.post("/", response_model=PageRead)
async def create_page(page: PageCreate, db: AsyncSession = Depends(get_db)):
    created_page = await crud_page.create(db, obj_in=page)
    return created_page


@router.get("/{page_id}", response_model=PageRead)
async def read_page(page_id: int, db: AsyncSession = Depends(get_db)):
    page = await crud_page.get_with_contents(db, id=page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@router.get("/", response_model=List[PageRead])
async def read_pages(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    pages = await crud_page.get_multi_with_contents(db, skip=skip, limit=limit)
    return pages

@router.put("/{page_id}", response_model=PageRead)
async def update_page(page_id: int, page: PageUpdate, db: AsyncSession = Depends(get_db)):
    db_page = await crud_page.get(db, id=page_id)
    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")
    updated_page = await crud_page.update(db, db_obj=db_page, obj_in=page)
    return updated_page

@router.delete("/{page_id}", response_model=dict)
async def delete_page(page_id: int, db: AsyncSession = Depends(get_db)):
    page = await crud_page.remove(db, id=page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return {"detail": "Page deleted successfully"}