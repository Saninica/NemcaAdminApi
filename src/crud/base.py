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

from src.database.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(
        self,
        model: Type[ModelType],
    ):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        """
        self.model = model

    async def transactional(db: AsyncSession, func: Callable, *args, **kwargs):
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
            load_relations: Optional[List[Any]] = None
    ) -> List[ModelType]:

        stmt = select(self.model)
        
        if load_relations:
            stmt = stmt.options(*[selectinload(rel) for rel in load_relations])
        
        if filters:
            for field, value in filters.items():
                stmt = stmt.where(getattr(self.model, field) == value)
        
        if sort_by:
            sort_column = getattr(self.model, sort_by)
            if sort_desc:
                stmt = stmt.order_by(desc(sort_column))
            else:
                stmt = stmt.order_by(asc(sort_column))
        
        stmt = stmt.offset(skip).limit(limit)

        print("Query:", stmt.compile(compile_kwargs={"literal_binds": True}))
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get(self, db: AsyncSession, id: Any, filters: Optional[List[Any]] = None,
    load_relations: Optional[List[Any]] = None) -> Optional[ModelType]:    
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
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100,
        load_relations: Optional[List[Any]] = None
    ) -> List[ModelType]:
        if load_relations:
            stmt = select(self.model).options(*[selectinload(rel) for rel in load_relations])
        else:
            stmt = select(self.model)
        result = await db.execute(stmt.offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_field(
        self,
        db: AsyncSession,
        field_name: str,
        value: Any,
        *,
        load_relations: Optional[List[Any]] = None
    ) -> Optional[ModelType]:
        """
        Generic method to get a single record by any field.

        **Parameters**

        * `field_name`: The name of the field to filter by.
        * `value`: The value to filter the field by.
        * `load_relations`: Optional list of relationships to load eagerly.
        """
        if load_relations:
            stmt = select(self.model).options(*[selectinload(rel) for rel in load_relations])
        else:
            stmt = select(self.model)
        stmt = stmt.where(getattr(self.model, field_name) == value)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def create(
        self, db: AsyncSession, *, obj_in: Optional[CreateSchemaType] = None, **kwargs
    ) -> ModelType:
        """
        Create a new record. If obj_in is provided, use it; otherwise, use kwargs.
        """
        print(obj_in)
        print("^^^^^^^^^^^^^^^^")
        if obj_in:
            obj_in_data = obj_in.dict(exclude_unset=True)
            db_obj = self.model(**obj_in_data)  # type: ignore
        else:
            db_obj = self.model(**kwargs)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Optional[Union[UpdateSchemaType, Dict[str, Any]]] = None
    ) -> ModelType:
        """
        Update an existing record. Can accept a Pydantic schema or a dict of fields.
        """
        if obj_in:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj