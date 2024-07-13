from abc import ABC, abstractmethod

from pyexpat import model
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession


class RepositoryBase(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, find_id: int):
        raise NotImplementedError


class Repository(RepositoryBase):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        mdl = self.model
        query_exec = await self.session.execute(insert(mdl).values(**data).returning(mdl))
        return query_exec.scalar()

    async def get_by_id(self, find_id: int) -> model:
        mdl = self.model
        query_exec = await self.session.execute(select(mdl).where(mdl.get_primary_key() == find_id))
        result: mdl = query_exec.scalars().first()
        return result

    async def delete_by_id(self, delete_id: int):
        mdl = self.model
        query_exec = await self.session.execute(delete(mdl).where(mdl.get_primary_key() == delete_id))
        await self.session.commit()
        return query_exec.rowcount

