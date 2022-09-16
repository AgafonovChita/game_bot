from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.services.repo.base_repo import SQLAlchemyRepo
from bot.services.repo import ScriptRepo


async def keyboard_control_script(repo: SQLAlchemyRepo):
    keyboard_admin = InlineKeyboardBuilder()
    if await repo.get_repo(ScriptRepo).get_script():
        keyboard_admin.add(
            InlineKeyboardButton(text="Изменить сценарий", callback_data="edit_script"),
            InlineKeyboardButton(text="Удалить сценарий", callback_data="delete_script"))
    else:
        keyboard_admin.add(
            InlineKeyboardButton(text="Создать сценарий", callback_data="create_script"))
    keyboard_admin.add(
        InlineKeyboardButton(text="Главное меню", callback_data="start_menu"))
    keyboard_admin.adjust(2, 2, repeat=True)
    return keyboard_admin.as_markup()



