from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from magic_filter import F

from bot.services.repo.base_repo import SQLAlchemyRepo
from bot.services.repo import ScriptRepo
from bot.filters.chat_type import ChatType
from bot.texts.private import tx_base
from bot.keyboards.private.control_script import kb_control_point

edit_script_router = Router()
edit_script_router.message.bind_filter(ChatType)


@edit_script_router.callback_query(F.data == "edit_script")
async def edit_script(call: types.CallbackQuery, bot: Bot, repo: SQLAlchemyRepo, state: FSMContext):
    await state.clear()
    await call.answer()
    await call.message.delete()
    game = await repo.get_repo(ScriptRepo).get_script()
    if game:
        await call.message.answer(text=await tx_base.get_description_script(repo=repo),
                                  reply_markup=await kb_control_point.keyboard_control_point(repo=repo))
        return
    await call.message.answer(text=tx_base.script_is_not_found)

