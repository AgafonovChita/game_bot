from aiogram.dispatcher.router import Router
from bot.filters.chat_type import ChatType
from magic_filter import F
from aiogram import types
from bot.services.repo import SQLAlchemyRepo, GameRepo, ScriptRepo
from aiogram.fsm.context import FSMContext
from bot.texts.private.control_game import tx_control_game
from bot.keyboards.private.control_game import kb_control_game
from .control_game_panel import control_game


teams_game_router = Router()
teams_game_router.message.bind_filter(ChatType)


@teams_game_router.callback_query(F.data == "get_teams")
async def stop_game(call: types.CallbackQuery, repo: SQLAlchemyRepo):
    await call.answer()
    await call.message.delete()
    await call.message.answer(text=await tx_control_game.teams_text(repo=repo),
                              reply_markup=await kb_control_game.return_menu())

