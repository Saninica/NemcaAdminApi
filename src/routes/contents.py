from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from src.schemas.page import PageContentCreate, PageContentRead, PageContentUpdate, PageContentMultiple
from src.crud.contents import crud_page_content
from src.dependencies import  get_db
from fastapi import UploadFile, File, Form
from src.models import PageContent
from src.schemas.queryparams import PageContentQueryParams


router = APIRouter()

def page_content_form(page_id: int = Form(...), website_id: int = Form(...), language_code: str = Form(...), title: str = Form(...), body: str = Form(...)):
    return PageContentCreate(page_id=page_id, website_id=website_id, language_code=language_code, title=title, body=body)


def page_content_update_form(website_id: int = Form(...), language_code: str = Form(...), title: str = Form(...), body: str = Form(...)):
    return PageContentUpdate(website_id=website_id, language_code=language_code, title=title, body=body)

@router.post("/", response_model=PageContentCreate)
async def create_page_content(page: PageContentCreate = Depends(page_content_form), cover_image: UploadFile = File(None), db: AsyncSession = Depends(get_db)):
    if cover_image:
        page.cover_image = await crud_page_content.upload_cover_image(cover_image)

    created_page = await crud_page_content.create(db, obj_in=page)
    return created_page


@router.get("/{content_id}/", response_model=PageContentRead)
async def read_page_content(content_id: int, db: AsyncSession = Depends(get_db)):
    page_content = await crud_page_content.get(db, id=content_id,  load_relations=[PageContent.page, PageContent.website] )
    
    if not page_content:
        raise HTTPException(status_code=404, detail="Page not found")
    return PageContentRead(
        id=page_content.id,
        page_id=page_content.page.id,  
        website_id=page_content.website.id,  
        language_code=page_content.language_code,
        title=page_content.title,
        body=page_content.body,
        cover_image= page_content.cover_image
    )

@router.get("/", response_model=List[PageContentMultiple])
async def read_page_contents(query: PageContentQueryParams = Depends(), db: AsyncSession = Depends(get_db)):
    res = []

    if query.website_id or query.page_id:
        res = await crud_page_content.get_multiple_contents(db, page_id=query.page_id, website_id=query.website_id,  language_code=query.language_code)

    else:
        pages = await crud_page_content.get_multi(db, skip=query.skip, limit=query.limit, load_relations=[PageContent.page, PageContent.website])
        res = [ {
            "id": page.id,
            "title": page.title,
            "body": page.body,
            "cover_image": page.cover_image,
            "page": page.page.name,
            "website": page.website.name,
            "language_code": page.language_code,
        } for page in pages]
    
    return res

@router.put("/{content_id}/", response_model=PageContentRead)
async def update_page_content(content_id: int, page: PageContentUpdate = Depends(page_content_update_form), cover_image: UploadFile = File(None), db: AsyncSession = Depends(get_db)):
    if cover_image:
        page.cover_image = await crud_page_content.upload_cover_image(cover_image, db)

    db_page = await crud_page_content.get(db, id=content_id)
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