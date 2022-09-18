from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from magic_filter import F

from bot.services.repo.base_repo import SQLAlchemyRepo
from bot.filters.chat_type import ChatType
from bot.keyboards.private.control_game import kb_control_game
from bot.texts.private.control_game import tx_control_game

control_game_panel_router = Router()
control_game_panel_router.message.bind_filter(ChatType)


@control_game_panel_router.callback_query(F.data == "control_game")
async def control_game(call: types.CallbackQuery, repo: SQLAlchemyRepo):
    await call.answer()
    await call.message.delete()
    await call.message.answer(text=await tx_control_game.control_game_text(repo=repo),
                              reply_markup=await kb_control_game.keyboard_control_game_panel(repo=repo))



