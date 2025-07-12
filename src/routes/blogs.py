from src.schemas.blogs import BlogCreate, BlogBase, BlogRead, BlogUpdate
from src.crud.blogs import crud_blog
from src.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User
from src.dependencies import get_current_user


router = APIRouter()


@router.get("/", response_model=list[BlogRead])
async def read_blogs(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        return await crud_blog.get_multi(db, filters={"website_id": current_user.websites[0].id})
        
    return await crud_blog.get_multi(db)


@router.post("/", response_model=BlogBase)
async def create_blog(data: BlogCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        data.website_id = current_user.websites[0].id

    return await crud_blog.create(db, obj_in=data)


@router.get("/{blog_id}", response_model=BlogRead)
async def read_blog(blog_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        return await crud_blog.get(db, id=blog_id, filters={"website_id": current_user.websites[0].id})
        
    return await crud_blog.get(db, id=blog_id)


@router.put("/{blog_id}", response_model=BlogBase)
async def update_blog(blog_id: int, blog: BlogUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        db_blog =  await crud_blog.get(db, id=blog_id, filters={"website_id": current_user.websites[0].id})
    else:
        db_blog =  await crud_blog.get(db, id=blog_id)
        
    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return await crud_blog.update(db, db_obj=db_blog, obj_in=blog)


@router.delete("/{blog_id}/")
async def delete_blog(blog_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        return await crud_blog.remove(db, id=blog_id, filters={"website_id": current_user.websites[0].id})
        
    return await crud_blog.remove(db, id=blog_id)
