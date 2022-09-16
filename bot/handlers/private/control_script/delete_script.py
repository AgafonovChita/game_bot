from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from magic_filter import F

from bot.keyboards.private.control_script import kb_base
from bot.keyboards.private.control_script import kb_control_script
from bot.services.repo.base_repo import SQLAlchemyRepo
from bot.services.repo import ScriptRepo
from bot.filters.chat_type import ChatType
from bot.models.states import DeleteScript
from bot.keyboards.private.control_script.kb_base import DeleteCallback
from bot.texts.private.control_script import tx_control_script
from bot.texts.private import tx_base

delete_script_router = Router()
delete_script_router.message.bind_filter(ChatType)


@delete_script_router.callback_query(F.data == "delete_script")
async def delete_script(call: types.CallbackQuery, bot: Bot, repo: SQLAlchemyRepo, state: FSMContext):
    await state.clear()
    await call.answer()
    await call.message.delete()
    game = await repo.get_repo(ScriptRepo).get_script()
    if game:
        await call.message.answer(text=await tx_base.get_description_script(repo=repo),
                                  reply_markup=await kb_base.delete_check_key())
        await state.set_state(DeleteScript.delete_script)
        return
    await call.message.answer(text=tx_base.script_is_not_found)


@delete_script_router.callback_query(DeleteCallback.filter(F.check), state=DeleteScript.delete_script)
async def delete_script(call: types.CallbackQuery, repo: SQLAlchemyRepo, state: FSMContext):
    await call.answer()
    await call.message.delete()
    delete_text = await tx_base.get_description_script(repo=repo)
    await repo.get_repo(ScriptRepo).delete_script()
    await call.message.answer(text="Сценарий успешно удалён",
                              reply_markup=await kb_control_script.keyboard_control_script(repo=repo))


@delete_script_router.callback_query(DeleteCallback.filter(F.check.is_(False)), state=DeleteScript.delete_script)
async def not_delete_script(call: types.CallbackQuery, bot: Bot, repo: SQLAlchemyRepo):
    await call.answer()
    await call.message.delete()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.message.answer(text=await tx_base.get_description_script(repo=repo),
                              reply_markup=await kb_control_script.keyboard_control_script(repo=repo))

