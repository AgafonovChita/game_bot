from aiogram.dispatcher.router import Router
from bot.filters.chat_type import ChatType
from magic_filter import F
from aiogram import types
from bot.services.repo import SQLAlchemyRepo, GameRepo, ScriptRepo
from aiogram.fsm.context import FSMContext
from bot.texts.private.control_game import tx_control_game
from bot.keyboards.private.control_game import kb_control_game
from .control_game_panel import control_game

cancel_game_router = Router()
cancel_game_router.message.bind_filter(ChatType)

@cancel_game_router.callback_query(F.data == "check_cancel_game")
async def stop_game(call: types.CallbackQuery, repo: SQLAlchemyRepo):
    await call.answer()
    await call.message.delete()
    await call.message.answer(text=tx_control_game.CANCEL_GAME,
                              reply_markup=await kb_control_game.check_cancel_game())
