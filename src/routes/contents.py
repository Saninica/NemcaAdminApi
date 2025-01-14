from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from src.schemas.page import PageContentCreate, PageContentRead, PageContentUpdate
from src.crud.contents import crud_page_content
from src.dependencies import get_current_user, get_db
from fastapi import UploadFile, File, Form


router = APIRouter()

def page_content_form(page_id: int = Form(...), website_id: int = Form(...), language_code: str = Form(...), title: str = Form(...), body: str = Form(...)):
    return PageContentCreate(page_id=page_id, website_id=website_id, language_code=language_code, title=title, body=body)


def page_content_update_form(website_id: int = Form(...), language_code: str = Form(...), title: str = Form(...), body: str = Form(...), cover_image: Optional[str] = None):
    return PageContentUpdate(website_id=website_id, language_code=language_code, title=title, body=body, cover_image=cover_image)

@router.post("/", response_model=PageContentCreate)
async def create_page_content(page: PageContentCreate = Depends(page_content_form), cover_image: UploadFile = File(None), db: AsyncSession = Depends(get_db)):
    if cover_image:
        page.cover_image = await crud_page_content.upload_cover_image(cover_image)

    created_page = await crud_page_content.create(db, obj_in=page)
    return created_page


@router.get("/{page_id}", response_model=PageContentRead)
async def read_page_content(page_id: int, db: AsyncSession = Depends(get_db)):
    page = await crud_page_content.get(db, id=page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@router.get("/", response_model=List[PageContentRead])
async def read_page_contents(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    pages = await crud_page_content.get_multi(db, skip=skip, limit=limit)
    return pages

@router.put("/{page_id}", response_model=PageContentRead)
async def update_page_content(page_id: int, page: PageContentUpdate = Depends(page_content_update_form), cover_image: UploadFile = File(None), db: AsyncSession = Depends(get_db)):
    if cover_image:
        page.cover_image = await crud_page_content.upload_cover_image(cover_image, db)

    db_page = await crud_page_content.get(db, id=page_id)
    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")

    
    updated_page = await crud_page_content.update(db, db_obj=db_page, obj_in=page)
    return updated_page

@router.delete("/{page_id}", response_model=dict)
async def delete_page_content(page_id: int, db: AsyncSession = Depends(get_db)):
    page = await crud_page_content.remove(db, id=page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return {"detail": "Page deleted successfully"}