from src.schemas.website import WebsiteCreate, WebsiteBase, WebsiteRead, WebsiteUpdate, ResponseSchema
from src.crud.website import crud_website
from src.dependencies import get_db, get_current_user
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from typing import List

router = APIRouter()


@router.get("/", response_model=List[WebsiteRead])
async def read_websites(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        return await crud_website.get_multi(db, filters={"id": current_user.websites[0].id})
    return await crud_website.get_multi(db)


@router.post("/", response_model=WebsiteBase)
async def create_website(name: str, domain_url: str, favicon_image: UploadFile = File(None), db: AsyncSession = Depends(get_db)):
    favicon_path = None

    if favicon_image:
        favicon_path = await crud_website.upload_favicon(favicon_image)

    website = WebsiteCreate(name=name, domain_url=domain_url, favicon_image=favicon_path)
    return await crud_website.create(db, obj_in=website)


@router.get("/{website_id}", response_model=WebsiteRead)
async def read_website(website_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        return await crud_website.get(db, id=website_id, filters={"id": current_user.websites[0].id})
    return await crud_website.get(db, id=website_id)


@router.put("/{website_id}/", response_model=WebsiteBase)
async def update_website(website_id: int, name: str, domain_url: str, favicon_image: UploadFile = File(None), db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        db_web = await crud_website.get(db, id=website_id, filters={"id": current_user.websites[0].id})
    else:
        db_web = await crud_website.get(db, id=website_id)

    favicon_path = db_web.favicon_image

    if not db_web:
        raise HTTPException(status_code=404, detail="Website not found")

    if favicon_image:
        favicon_path = await crud_website.upload_favicon(favicon_image)

    website = WebsiteUpdate(name=name, domain_url=domain_url, favicon_image=favicon_path)

    return await crud_website.update(db, db_obj=db_web, obj_in=website)


@router.delete("/{website_id}/", response_model=WebsiteBase)
async def delete_website(website_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        db_web = await crud_website.get(db, id=website_id, filters={"id": current_user.websites[0].id})
    else:
        db_web = await crud_website.get(db, id=website_id)

    if not db_web:
        raise HTTPException(status_code=404, detail="Website not found")
    return await crud_website.remove(db, id=website_id)


@router.get("/all-info/{website_id}/{language_code}/", response_model=ResponseSchema)
async def read_website_info(website_id: int, language_code: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False and website_id != current_user.websites[0].id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    return await crud_website.get_all_website_info(db, website_id=website_id, language_code=language_code)