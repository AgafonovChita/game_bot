from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData




async def generate_help_key():
    keyboard_admin = InlineKeyboardBuilder()
    keyboard_admin.add(
        InlineKeyboardButton(text="Показать подсказку", callback_data="help_me"),
    )
    keyboard_admin.adjust(1, repeat=True)
    return keyboard_admin.as_markup()

