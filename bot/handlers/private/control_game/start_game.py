from aiogram.dispatcher.router import Router
from bot.filters.chat_type import ChatType
from magic_filter import F
from aiogram import types, Bot
from bot.services.repo import SQLAlchemyRepo, GameRepo, ScriptRepo
from aiogram.fsm.context import FSMContext
from bot.texts.private.control_game import tx_control_game
from bot.keyboards.private.control_game import kb_control_game
from bot.engine import game_api
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.storage.memory import MemoryStorage

start_game_router = Router()
start_game_router.message.bind_filter(ChatType)


@start_game_router.callback_query(F.data == "start_game")
async def start_game(call: types.CallbackQuery, repo: SQLAlchemyRepo,
                     bot: Bot, scheduler: AsyncIOScheduler):
    await call.answer()
    await call.message.delete()
    idx = await repo.get_repo(ScriptRepo).get_script_id()
    await repo.get_repo(GameRepo).start_game(game_id=idx)
    scheduler.start()
    await game_api.start_game(repo=repo, bot=bot, scheduler=scheduler)
    await call.message.answer(text=await tx_control_game.control_game_text(repo=repo),
                              reply_markup=await kb_control_game.keyboard_control_game_panel(repo=repo))




