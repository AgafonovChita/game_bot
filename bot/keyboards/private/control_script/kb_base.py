from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class DeleteCallback(CallbackData, prefix="delete"):
    check: bool


async def delete_check_key():
    keyboard_admin = InlineKeyboardBuilder()
    keyboard_admin.add(
        InlineKeyboardButton(text="Удалить", callback_data=DeleteCallback(check=True).pack()),
        InlineKeyboardButton(text="Отменить", callback_data=DeleteCallback(check=False).pack()))
    keyboard_admin.adjust(2, repeat=True)
    return keyboard_admin.as_markup()
