from aiogram.dispatcher.router import Router
from bot.filters.chat_type import ChatType

protocol_game_router = Router()
protocol_game_router.message.bind_filter(ChatType)
