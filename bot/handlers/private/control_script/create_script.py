import random

from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from magic_filter import F

from bot.services.repo.base_repo import SQLAlchemyRepo
from bot.services.repo import ScriptRepo
from bot.filters.chat_type import ChatType
from bot.models.states import CreateGame
from bot.texts.private.control_script import tx_control_script
from bot.keyboards.private.control_script import kb_control_point

create_script_router = Router()
create_script_router.message.bind_filter(ChatType)


@create_script_router.callback_query(F.data == "create_script")
async def check_create_script(call: types.CallbackQuery, state: FSMContext, repo: SQLAlchemyRepo):
    await state.clear()
    await call.answer()
    await call.message.delete()
    await call.message.answer(text=tx_control_script.create_script)
    await state.set_state(CreateGame.name_game)


@create_script_router.message(state=CreateGame.name_game)
async def save_new_script(message: types.Message, repo: SQLAlchemyRepo, bot: Bot, state: FSMContext):
    await repo.get_repo(ScriptRepo).add_script(script_id=random.randint(1, 10000),
                                               script_name=message.text)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
    await message.answer(await tx_control_script.script_is_creating(name_game=message.text,
                                                                    repo=repo),
                         reply_markup=await kb_control_point.keyboard_control_point(repo=repo))
    await state.clear()


