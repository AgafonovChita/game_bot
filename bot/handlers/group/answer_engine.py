from aiogram import types, Bot
from aiogram.dispatcher.router import Router

from magic_filter import F
from bot.filters import TagBot, ChatType, GameState

from bot.utils.parse import parse_answer, answer_is_valid
from bot.services.repo import SQLAlchemyRepo
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.texts.game_engine import tx_game_engine
from bot import engine
import datetime

answer_router = Router()
answer_router.message.bind_filter(TagBot)
answer_router.message.bind_filter(ChatType)
answer_router.message.bind_filter(GameState)


@answer_router.message(game_state=2, tag_bot=True)
async def message_for_bot(message: types.Message, repo: SQLAlchemyRepo, bot: Bot, scheduler: AsyncIOScheduler):
    """Сообщения обращённые к боту - т.е. варианты ответов"""
    if await answer_is_valid(text=message.text, bot=bot):
        answer = await parse_answer(message.text)
        await engine.check_current_answer(answer_text=answer, team_idx=message.chat.id,
                                          bot=bot, repo=repo,
                                          message=message, scheduler=scheduler)
        return
    await message.reply(text=tx_game_engine.ANSWER_IS_EMPTY)


@answer_router.message(game_state=1, tag_bot=True)
async def message_for_bot(message: types.Message, bot: Bot):
    if await answer_is_valid(text=message.text, bot=bot):
        await message.answer(text=tx_game_engine.GAME_NOT_START)
        return
    await message.reply(text=tx_game_engine.ANSWER_IS_EMPTY)

