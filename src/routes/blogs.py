from src.schemas.blogs import BlogCreate, BlogBase, BlogRead, BlogUpdate
from src.crud.blogs import crud_blog
from src.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/", response_model=list[BlogRead])
async def read_blogs(db: AsyncSession = Depends(get_db)):
    return await crud_blog.get_multi(db)


@router.post("/", response_model=BlogBase)
async def create_blog(data: BlogCreate, db: AsyncSession = Depends(get_db)):
    return await crud_blog.create(db, obj_in=data)


@router.get("/{blog_id}", response_model=BlogRead)
async def read_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    return await crud_blog.get(db, id=blog_id)


@router.put("/{blog_id}", response_model=BlogBase)
async def update_blog(blog_id: int, title: str, content: str, db: AsyncSession = Depends(get_db)):
    db_blog = await crud_blog.get(db, id=blog_id)

    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog = BlogUpdate(title=title, content=content)

    return await crud_blog.update(db, db_obj=db_blog, obj_in=blog)


@router.delete("/{blog_id}")
async def delete_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    return await crud_blog.remove(db, id=blog_id)
