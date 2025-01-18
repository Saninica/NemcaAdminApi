from src.schemas.website import WebsiteCreate, WebsiteBase, WebsiteRead, WebsiteUpdate
from src.crud.website import crud_website
from src.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/", response_model=list[WebsiteRead])
async def read_websites(db: AsyncSession = Depends(get_db)):
    return await crud_website.get_multi(db)


@router.post("/", response_model=WebsiteBase)
async def create_website(name: str, domain_url: str, favicon_image: UploadFile = File(None), db: AsyncSession = Depends(get_db)):
    favicon_path = None

    if favicon_image:
        favicon_path = await crud_website.upload_favicon(favicon_image)

    website = WebsiteCreate(name=name, domain_url=domain_url, favicon_image=favicon_path)
    return await crud_website.create(db, obj_in=website)


@router.get("/{website_id}", response_model=WebsiteRead)
async def read_website(website_id: int, db: AsyncSession = Depends(get_db)):
    return await crud_website.get(db, id=website_id)


@router.put("/{website_id}/", response_model=WebsiteBase)
async def update_website(website_id: int, name: str, domain_url: str, favicon_image: UploadFile = File(None), db: AsyncSession = Depends(get_db)):
    db_web = await crud_website.get(db, id=website_id)
    favicon_path = db_web.favicon_image

    if not db_web:
        raise HTTPException(status_code=404, detail="Website not found")

    if favicon_image:
        favicon_path = await crud_website.upload_favicon(favicon_image)

    website = WebsiteUpdate(name=name, domain_url=domain_url, favicon_image=favicon_path)

    return await crud_website.update(db, db_obj=db_web, obj_in=website)


@router.delete("/{website_id}/", response_model=WebsiteBase)
async def delete_website(website_id: int, db: AsyncSession = Depends(get_db)):
    db_web = await crud_website.get(db, id=website_id)
    if not db_web:
        raise HTTPException(status_code=404, detail="Website not found")
    return await crud_website.remove(db, id=website_id)