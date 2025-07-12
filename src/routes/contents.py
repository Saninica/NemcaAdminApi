from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from typing import List, Optional
from src.schemas.page import PageContentCreate, PageContentRead, PageContentUpdate, PaginatedPageContentResponse
from src.crud.contents import crud_page_content
from src.dependencies import  get_db, get_current_user
from fastapi import UploadFile, File, Form
from src.models import PageContent, User
from src.schemas.queryparams import PageContentQueryParams



router = APIRouter()

def page_content_form(page_id: int = Form(...), language_id: int = Form(...), title: str = Form(...), body: str = Form(...), website_id: Optional[int] = Form(None),
    price: Optional[float] = Form(None)):
    return PageContentCreate(page_id=page_id, language_id=language_id, website_id=website_id, title=title, body=body, price=price)


def page_content_update_form(language_id: int = Form(...), title: str = Form(...), body: str = Form(...), price: Optional[float] = Form(None)):
    return PageContentUpdate(language_id=language_id, title=title, body=body, price=price)

@router.post("/", response_model=PageContentCreate)
async def create_page_content(page: PageContentCreate = Depends(page_content_form), cover_images: List[UploadFile] = File(None), db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if cover_images:
        page.cover_images = await crud_page_content.upload_cover_images(cover_images)

    if current_user.is_superuser is False:
        page.website_id = current_user.websites[0].id

    created_page = await crud_page_content.create(db, obj_in=page)
    return created_page


@router.get("/{content_id}/", response_model=PageContentRead)
async def read_page_content(content_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        page_content = await crud_page_content.get(db, id=content_id,  load_relations=[PageContent.page, PageContent.website, PageContent.language] , filters={"website_id": current_user.websites[0].id})
    else:
        page_content = await crud_page_content.get(db, id=content_id,  load_relations=[PageContent.page, PageContent.website, PageContent.language])
    
    if not page_content:
        raise HTTPException(status_code=404, detail="Page not found")
    return PageContentRead(
        id=page_content.id,
        page_id=page_content.page.id,  
        website_id=page_content.website.id,  
        language_id=page_content.language.id,
        title=page_content.title,
        body=page_content.body,
        cover_images= page_content.cover_images or []
    )

@router.get("/", response_model=PaginatedPageContentResponse)
async def read_page_contents(query: PageContentQueryParams = Depends(), db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = []

    if query.website_id or query.page_id:
        if current_user.is_superuser is False: 
           response = await crud_page_content.get_multi(db, skip=query.skip, limit=query.limit, load_relations=[PageContent.page, PageContent.website, PageContent.language],  
           filters={"website_id": current_user.websites[0].id, "page_id": query.page_id, "language_id": query.language_id})
        else:
           response = await crud_page_content.get_multi(db, skip=query.skip, limit=query.limit, load_relations=[PageContent.page, PageContent.website, PageContent.language],  
           filters={"page_id": query.page_id, "language_id": query.language_id, "website_id": query.website_id})

    else:
        response = await crud_page_content.get_multi(db, skip=query.skip, limit=query.limit, 
        load_relations=[PageContent.page, PageContent.website, PageContent.language],
        filters={"website_id": current_user.websites[0].id})
    
    res = [ {
        "id": page.id,
        "title": page.title,
        "body": page.body,
        "cover_images": page.cover_images or [],
        "page": page.page.name,
        "website": page.website.name,
        "language_code": page.language.code,
    } for page in response]
    
    total_stmt = select(func.count()).select_from(PageContent)
    total_result = await db.execute(total_stmt)
    total = total_result.scalar_one()

    return PaginatedPageContentResponse(
        items=res,
        total=total,
        limit=query.limit,
        skip=query.skip
    )

@router.put("/{content_id}/", response_model=PageContentRead)
async def update_page_content(content_id: int, page: PageContentUpdate = Depends(page_content_update_form), cover_images: List[UploadFile] = File(None), db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if cover_images:
        page.cover_images = await crud_page_content.upload_cover_images(cover_images)

    if current_user.is_superuser is False:
        page.website_id = current_user.websites[0].id
        db_page = await crud_page_content.get(db, id=content_id, filters={"website_id": current_user.websites[0].id})
    else:
        db_page = await crud_page_content.get(db, id=content_id)

    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")

    
    updated_page = await crud_page_content.update(db, db_obj=db_page, obj_in=page)
    return updated_page

@router.delete("/{content_id}/", response_model=dict)
async def delete_page_content(content_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        page = await crud_page_content.remove(db, id=content_id, filters={"website_id": current_user.websites[0].id})
    else:
        page = await crud_page_content.remove(db, id=content_id)
    
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return {"detail": "Page deleted successfully"}