
from aiogram import types
from magic_filter import F

from aiogram.dispatcher.router import Router

from bot.keyboards.private.control_script import kb_control_point
from bot.texts.private.control_script.control_point import tx_control_point
from bot.filters.chat_type import ChatType

from bot.services.repo.base_repo import SQLAlchemyRepo

view_points_router = Router()
view_points_router.message.bind_filter(ChatType)


@view_points_router.callback_query(F.data == "view_points")
async def view_points(call: types.CallbackQuery, repo: SQLAlchemyRepo):
    await call.answer()
    await call.message.delete()
    await call.message.answer(text=await tx_control_point.get_list_points(repo=repo),
                              reply_markup=await kb_control_point.delete_menu_key())

