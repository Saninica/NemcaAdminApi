from src.schemas.announcement import AnnouncementCreate, AnnouncementUpdate, Announcement
from src.crud.announcement import crud_announcement
from src.dependencies import get_db
from fastapi import Depends
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, File
from fastapi import Form


router = APIRouter()

def announcement_create_form(page_id: int = Form(...), website_id: int = Form(...), 
    language_code: str = Form(...), title: str = Form(...), body: str = Form(...),
    start_date: str = Form(...), end_date: str = Form(...)):
    return AnnouncementCreate(page_id=page_id, website_id=website_id, language_code=language_code, 
    title=title, body=body,cover_image="",
    start_date=start_date, end_date=end_date)


@router.get("/", response_model=list[Announcement])
async def read_announcements(db: AsyncSession = Depends(get_db)):
    return await crud_announcement.get_multi(db)


@router.get("/{announcement_id}/", response_model=Announcement)
async def read_announcement(announcement_id: int, db: AsyncSession = Depends(get_db)):
    return await crud_announcement.get(db, id=announcement_id)


@router.post("/", response_model=Announcement)
async def create_announcement(announcement: AnnouncementCreate = Depends(announcement_create_form), cover_image: UploadFile = File(None), db: AsyncSession = Depends(get_db)):
    if cover_image:
        announcement.cover_image = await crud_announcement.upload_cover_image(cover_image)

    return await crud_announcement.create(db, obj_in=announcement)


@router.put("/{announcement_id}/", response_model=Announcement)
async def update_announcement(announcement_id: int, announcement: AnnouncementUpdate, db: AsyncSession = Depends(get_db)):
    db_announcement = await crud_announcement.get(db, id=announcement_id)
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    return await crud_announcement.update(db, db_obj=db_announcement, obj_in=announcement)

@router.delete("/{announcement_id}/", response_model=Announcement)
async def delete_announcement(announcement_id: int, db: AsyncSession = Depends(get_db)):
    return await crud_announcement.remove(db, id=announcement_id)