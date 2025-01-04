from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.schemas.page import PageContentCreate, PageContentRead, PageContentUpdate
from src.crud.contents import crud_page_content
from src.dependencies import get_current_user, get_db


router = APIRouter()

@router.post("/", response_model=PageContentCreate,  dependencies=[Depends(get_current_user)])
async def create_page_content(page: PageContentCreate, db: AsyncSession = Depends(get_db)):
    created_page = await crud_page_content.create(db, obj_in=page)
    return created_page


@router.get("/{page_id}", response_model=PageContentRead, dependencies=[Depends(get_current_user)])
async def read_page_content(page_id: int, db: AsyncSession = Depends(get_db)):
    page = await crud_page_content.get(db, id=page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@router.get("/", response_model=List[PageContentRead], dependencies=[Depends(get_current_user)])
async def read_page_contents(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    pages = await crud_page_content.get_multi(db, skip=skip, limit=limit)
    return pages

@router.put("/{page_id}", response_model=PageContentRead, dependencies=[Depends(get_current_user)])
async def update_page_content(page_id: int, page: PageContentUpdate, db: AsyncSession = Depends(get_db)):
    db_page = await crud_page_content.get(db, id=page_id)
    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")
    updated_page = await crud_page_content.update_with_contents(db, db_obj=db_page, obj_in=page)
    return updated_page

@router.delete("/{page_id}", response_model=dict, dependencies=[Depends(get_current_user)])
async def delete_page_content(page_id: int, db: AsyncSession = Depends(get_db)):
    page = await crud_page_content.remove(db, id=page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return {"detail": "Page deleted successfully"}