from src.schemas.metatags import MetatagsCreate, MetatagsUpdate, Metatags
from src.crud.metatags import crud_metatags
from src.dependencies import get_db
from fastapi import Depends
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User
from src.dependencies import get_current_user


router = APIRouter()    

@router.get("/", response_model=list[Metatags])
async def read_metatags(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        return await crud_metatags.get_multi(db, filters={"website_id": current_user.websites[0].id})
    else:
        return await crud_metatags.get_multi(db)


@router.get("/{metatag_id}", response_model=Metatags)
async def read_metatag(metatag_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        db_metatag = await crud_metatags.get(db, id=metatag_id, filters={"website_id": current_user.websites[0].id})
    else:
        db_metatag = await crud_metatags.get(db, id=metatag_id)
    
    if not db_metatag:
        raise HTTPException(status_code=404, detail="Metatag not found")
    return db_metatag


@router.post("/", response_model=Metatags)
async def create_metatag(metatag: MetatagsCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        metatag.website_id = current_user.websites[0].id
    return await crud_metatags.create(db, obj_in=metatag)


@router.put("/{metatag_id}", response_model=Metatags)
async def update_metatag(metatag_id: int, metatag: MetatagsUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        db_metatag = await crud_metatags.get(db, id=metatag_id, filters={"website_id": current_user.websites[0].id})
    else:
        db_metatag = await crud_metatags.get(db, id=metatag_id)
    
    if not db_metatag:
        raise HTTPException(status_code=404, detail="Metatag not found")
    updated_metatag = await crud_metatags.update(db, db_obj=db_metatag, obj_in=metatag)
    return updated_metatag

@router.delete("/{metatag_id}/", response_model=Metatags)
async def delete_metatag(metatag_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_superuser is False:
        db_metatag = await crud_metatags.get(db, id=metatag_id, filters={"website_id": current_user.websites[0].id})
    else:
        db_metatag = await crud_metatags.get(db, id=metatag_id)
    
    if not db_metatag:
        raise HTTPException(status_code=404, detail="Metatag not found")
        
    return await crud_metatags.remove(db, id=metatag_id)