
from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from bot.services.repo.base_repo import SQLAlchemyRepo
from bot.filters.chat_type import ChatType
from magic_filter import F
from bot.keyboards.private.admin_key import keyboard_admin_panel
from bot.texts.private import tx_admin

admin_router = Router()
admin_router.message.bind_filter(ChatType)


@admin_router.message(commands="start", chat_type='private')
async def message_for_bot(message: types.Message, state: FSMContext, bot: Bot, repo: SQLAlchemyRepo):
    await message.answer(text=tx_admin.admin_start_panel,
                         reply_markup=await keyboard_admin_panel(repo=repo))


@admin_router.callback_query(F.data == "start_menu")
async def get_start_menu(call: types.CallbackQuery, bot: Bot, repo: SQLAlchemyRepo):
    await call.answer()
    await call.message.delete()
    await call.message.answer(text=tx_admin.admin_start_panel,
                              reply_markup=await keyboard_admin_panel(repo=repo))



