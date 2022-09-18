from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.services.repo.base_repo import SQLAlchemyRepo


class Scheduler(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler) -> None:
        super().__init__()
        self.scheduler = scheduler

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        data['scheduler'] = self.scheduler

        result = await handler(event, data)

        data.pop('scheduler')

        return result
