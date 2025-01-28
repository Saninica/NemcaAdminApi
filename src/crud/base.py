from typing import (
    Generic,
    Type,
    TypeVar,
    List,
    Optional,
    Any,
    Union,
    Callable,
    Dict,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import asc, desc
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from src.database.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def transactional(self, db: AsyncSession, func: Callable, *args, **kwargs):
        try:
            result = await func(db, *args, **kwargs)
            await db.commit()
            return result
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    async def get_filtered(
        self,
        db: AsyncSession,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
        sort_desc: bool = False,
        skip: int = 0,
        limit: int = 100,
        load_relations: Optional[List[Any]] = None,
    ) -> List[ModelType]:
        stmt = select(self.model)
        if load_relations:
            stmt = stmt.options(*[selectinload(rel) for rel in load_relations])
        if filters:
            for field, value in filters.items():
                stmt = stmt.where(getattr(self.model, field) == value)
        if sort_by:
            sort_column = getattr(self.model, sort_by)
            stmt = stmt.order_by(desc(sort_column) if sort_desc else asc(sort_column))
        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get(
        self,
        db: AsyncSession,
        id: Any = 0,
        filters: Optional[Dict[str, Any]] = None,
        load_relations: Optional[List[Any]] = None,
    ) -> Optional[ModelType]:
        stmt = select(self.model)
        if load_relations:
            stmt = stmt.options(*[selectinload(rel) for rel in load_relations])
        if id:
            stmt = stmt.where(self.model.id == id)
        if filters:
            for field, value in filters.items():
                stmt = stmt.where(getattr(self.model, field) == value)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        load_relations: Optional[List[Any]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[ModelType]:
        stmt = select(self.model)
        if load_relations:
            stmt = stmt.options(*[selectinload(rel) for rel in load_relations])
        if filters:
            for field, value in filters.items():
                stmt = stmt.where(getattr(self.model, field) == value)
        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_by_field(
        self,
        db: AsyncSession,
        field_name: str,
        value: Any,
        *,
        load_relations: Optional[List[Any]] = None,
    ) -> Optional[ModelType]:
        stmt = select(self.model)
        if load_relations:
            stmt = stmt.options(*[selectinload(rel) for rel in load_relations])
        stmt = stmt.where(getattr(self.model, field_name) == value)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: Optional[CreateSchemaType] = None,
        **kwargs,
    ) -> ModelType:
        async def create_operation(db: AsyncSession):
            obj_in_data = obj_in.model_dump(exclude_unset=True) if obj_in else kwargs
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            await db.flush()
            await db.refresh(db_obj)
            return db_obj
        
        return await self.transactional(db, create_operation)

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Optional[Union[UpdateSchemaType, Dict[str, Any]]] = None,
    ) -> ModelType:
        async def update_operation(db: AsyncSession):
            if obj_in:
                update_data = obj_in.dict(exclude_unset=True) if not isinstance(obj_in, dict) else obj_in
                for field, value in update_data.items():
                    if hasattr(db_obj, field):
                        setattr(db_obj, field, value)
                db.add(db_obj)
                await db.flush()
                await db.refresh(db_obj)
            return db_obj
        
        return await self.transactional(db, update_operation)

    async def remove(
        self,
        db: AsyncSession,
        *,
        id: int,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Optional[ModelType]:
        async def remove_operation(db: AsyncSession):
            obj = await self.get(db, id, filters=filters)
            if obj:
                await db.delete(obj)
            return obj
        
        return await self.transactional(db, remove_operation)