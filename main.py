import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from aiogram.fsm.storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.db.base import Base

from bot.handlers.private.admin import admin_router
from bot.handlers.group.local import local_router
from bot.handlers.private.my_chat import my_chat_router
from bot.handlers.private.control_script import control_script_router
from bot.handlers.private.control_game import control_game_router
from bot.handlers.group import game_engine_router

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from bot.middlewares import Repository, Scheduler

from bot.config import Config

logger = logging.getLogger(__name__)


async def get_scheduler(sqlite_name: str):
    #job_stores = {'default': SQLAlchemyJobStore(url=f'sqlite:///{sqlite_name}')}
    scheduler = AsyncIOScheduler(timezone="Europe/Berlin")
    return scheduler


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        stream=sys.stdout)

    logger.info("Starting my_chat")

    bot = Bot(Config.bot_token, parse_mode="HTML")
    storage = MemoryStorage()

    scheduler = await get_scheduler(sqlite_name=Config.db_name)

    engine = create_async_engine(f"{Config.db_url}", future=True, echo=False)
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    dp = Dispatcher(storage=storage)

    """private routers"""
    admin_router.message.outer_middleware(Repository(async_session=async_session))
    admin_router.callback_query.outer_middleware(Repository(async_session=async_session))
    local_router.message.outer_middleware(Repository(async_session=async_session))

    my_chat_router.message.outer_middleware(Repository(async_session=async_session))
    my_chat_router.my_chat_member.outer_middleware(Repository(async_session=async_session))

    control_script_router.message.outer_middleware(Repository(async_session=async_session))
    control_script_router.callback_query.outer_middleware(Repository(async_session=async_session))

    control_game_router.message.outer_middleware(Repository(async_session=async_session))
    control_game_router.callback_query.outer_middleware(Repository(async_session=async_session))
    control_game_router.message.outer_middleware(Scheduler(scheduler=scheduler))
    control_game_router.callback_query.outer_middleware(Scheduler(scheduler=scheduler))

    game_engine_router.message.outer_middleware(Repository(async_session=async_session))
    game_engine_router.callback_query.outer_middleware(Repository(async_session=async_session))
    game_engine_router.message.outer_middleware(Scheduler(scheduler=scheduler))
    game_engine_router.callback_query.outer_middleware(Scheduler(scheduler=scheduler))

    dp.include_router(admin_router)
    dp.include_router(local_router)
    dp.include_router(my_chat_router)
    dp.include_router(control_script_router)
    dp.include_router(control_game_router)
    dp.include_router(game_engine_router)

    try:
        await bot.get_updates(offset=-1)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Exit")
