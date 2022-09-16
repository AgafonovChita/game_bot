from aiogram.dispatcher.router import Router
from bot.filters.chat_type import ChatType
from .answer_engine import answer_router

game_engine_router = Router()
game_engine_router.message.bind_filter(ChatType)

game_engine_router.include_router(answer_router)



