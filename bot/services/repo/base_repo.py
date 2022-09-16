from sqlalchemy.ext.asyncio import AsyncSession
from functools import lru_cache
from typing import Type, TypeVar

from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class BaseSQLAlchemyRepo(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session


T = TypeVar("T", bound=BaseSQLAlchemyRepo)


class SQLAlchemyRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    @lru_cache()
    def get_repo(self, repo: Type[T]) -> T:
        return repo(self._session)

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()