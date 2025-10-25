from typing import Generic, List, Type, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def _base_query(self) -> Select[ModelType]:
        return select(self.model)

    async def get_by_id(self, obj_id: int, session: AsyncSession) -> ModelType:
        obj = await session.execute(
            self._base_query().where(self.model.id == obj_id)
        )
        return obj.scalars().first()

    async def list_all(self, session: AsyncSession) -> List[ModelType]:
        objs = await session.execute(self._base_query())
        return objs.scalars().all()
