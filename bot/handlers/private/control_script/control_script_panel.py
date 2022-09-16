from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from magic_filter import F

from bot.keyboards.private.control_script import kb_control_script
from bot.services.repo.base_repo import SQLAlchemyRepo
from bot.filters.chat_type import ChatType
from bot.texts.private import tx_base

control_script_panel_router = Router()
control_script_panel_router.message.bind_filter(ChatType)


@control_script_panel_router.callback_query(F.data == "control_script")
async def start_game(call: types.CallbackQuery, repo: SQLAlchemyRepo, state: FSMContext):
    await state.clear()
    await call.answer()
    await call.message.delete()
    await call.message.answer(text=await tx_base.get_description_script(repo=repo),
                              reply_markup=await kb_control_script.keyboard_control_script(repo=repo))





