from src.schemas.announcement import AnnouncementCreate, AnnouncementUpdate, Announcement
from src.crud.announcement import crud_announcement
from src.dependencies import get_db, get_current_user
from fastapi import Depends
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, File
from fastapi import Form
from typing import Optional
from src.models.user import User


router = APIRouter()

def announcement_create_form(page_id: int = Form(...), 
    language_id: int = Form(...), title: str = Form(...), body: str = Form(...),
    start_date: str = Form(...), end_date: str = Form(...), website_id: Optional[int] = Form(None)):
    return AnnouncementCreate(page_id=page_id, language_id=language_id, 
    title=title, body=body,cover_image="",
    start_date=start_date, end_date=end_date, website_id=website_id)


@router.get("/", response_model=list[Announcement])
async def read_announcements(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        return await crud_announcement.get_multi(db, filters={"website_id": current_user.websites[0].id})
    return await crud_announcement.get_multi(db)


@router.get("/{announcement_id}/", response_model=Announcement)
async def read_announcement(announcement_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        return await crud_announcement.get(db, id=announcement_id, filters={"website_id": current_user.websites[0].id})
    return await crud_announcement.get(db, id=announcement_id)


@router.post("/", response_model=Announcement)
async def create_announcement(announcement: AnnouncementCreate = Depends(announcement_create_form), cover_image: UploadFile = File(None), 
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if cover_image:
        announcement.cover_image = await crud_announcement.upload_cover_image(cover_image)

    if current_user.is_superuser is False:
        announcement.website_id = current_user.websites[0].id
    else:
        announcement.website_id = announcement.website_id

    created_announcement = await crud_announcement.create(db, obj_in=announcement)
    return created_announcement


@router.put("/{announcement_id}/", response_model=Announcement)
async def update_announcement(announcement_id: int, announcement: AnnouncementUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_announcement = await crud_announcement.get(db, id=announcement_id)
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    if current_user.is_superuser is False:
        return await crud_announcement.update(db, db_obj=db_announcement, obj_in=announcement, filters={"website_id": current_user.websites[0].id})
        
    return await crud_announcement.update(db, db_obj=db_announcement, obj_in=announcement)


@router.delete("/{announcement_id}/", response_model=Announcement)
async def delete_announcement(announcement_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_announcement = await crud_announcement.get(db, id=announcement_id)
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    if current_user.is_superuser is False:
        return await crud_announcement.remove(db, id=announcement_id, filters={"website_id": current_user.websites[0].id})
        
    return await crud_announcement.remove(db, id=announcement_id)