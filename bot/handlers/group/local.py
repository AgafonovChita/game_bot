from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from bot.filters.tag_bot import TagBot
from bot.filters.chat_type import ChatType


local_router = Router()
local_router.message.bind_filter(TagBot)
local_router.message.bind_filter(ChatType)


@local_router.message(tag_bot=False, chat_type="supergroup")
async def message_not_for_bot(message: types.Message, state: FSMContext, bot: Bot):
    """Перписка игроков не обращённая к боту"""
    pass
