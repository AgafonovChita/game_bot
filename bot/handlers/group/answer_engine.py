from aiogram import types, Bot
from aiogram.dispatcher.router import Router

from magic_filter import F
from bot.filters import TagBot, ChatType, GameState

from bot.utils.parse import parse_answer
from bot.services.repo import SQLAlchemyRepo
from bot import engine

answer_router = Router()
answer_router.message.bind_filter(TagBot)
answer_router.message.bind_filter(ChatType)
answer_router.message.bind_filter(GameState)


@answer_router.message(game_state=2, tag_bot=True)
async def message_for_bot(message: types.Message, repo: SQLAlchemyRepo, bot: Bot):
    """Сообщения обращённые к боту - т.е. варианты ответов"""
    answer = await parse_answer(message.text)
    await engine.check_answer(answer_text=answer,
                              team_idx=message.chat.id,
                              repo=repo,
                              bot=bot)

