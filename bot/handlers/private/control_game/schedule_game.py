from aiogram.dispatcher.router import Router
from bot.filters.chat_type import ChatType
from magic_filter import F
from aiogram import types
from bot.services.repo import SQLAlchemyRepo, GameRepo, ScriptRepo
from aiogram.fsm.context import FSMContext
from bot.texts.private.control_game import tx_control_game
from bot.keyboards.private.control_game import kb_control_game

schedule_game_router = Router()
schedule_game_router.message.bind_filter(ChatType)


@schedule_game_router.callback_query(F.data == "schedule_game")
async def start_game(call: types.CallbackQuery, repo: SQLAlchemyRepo, state: FSMContext):
    await call.answer()
    await call.message.delete()
    idx = await repo.get_repo(ScriptRepo).get_script_id()
    await repo.get_repo(GameRepo).schedule_game(game_id=idx)
    await call.message.answer(text=await tx_control_game.control_game_text(repo=repo),
                              reply_markup=await kb_control_game.keyboard_control_game_panel(repo=repo))

