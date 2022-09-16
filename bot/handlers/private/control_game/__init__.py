from aiogram.dispatcher.router import Router
from bot.filters.chat_type import ChatType

from .protocol_game import protocol_game_router
from .control_game_panel import control_game_panel_router
from .schedule_game import schedule_game_router
from .start_game import start_game_router
from .stop_game import stop_game_router
from .reset_game import reset_game_router
from .teams_game import teams_game_router

control_game_router = Router()
control_game_router.message.bind_filter(ChatType)

control_game_router.include_router(protocol_game_router)
control_game_router.include_router(control_game_panel_router)
control_game_router.include_router(schedule_game_router)
control_game_router.include_router(start_game_router)
control_game_router.include_router(stop_game_router)
control_game_router.include_router(reset_game_router)
control_game_router.include_router(teams_game_router)


