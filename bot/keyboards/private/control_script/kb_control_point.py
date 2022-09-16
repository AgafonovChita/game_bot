from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.services.repo.base_repo import SQLAlchemyRepo
from bot.services.repo import PointRepo


class TypePoint(CallbackData, prefix="type_point"):
    prefix: str
    is_img: bool


async def keyboard_control_point(repo: SQLAlchemyRepo):
    keyboard_admin = InlineKeyboardBuilder()
    keyboard_admin.add(
        InlineKeyboardButton(text="Добавить задание", callback_data="add_point"))
    if await repo.get_repo(PointRepo).get_points_list():
        keyboard_admin.add(
            InlineKeyboardButton(text="Просмотреть задания", callback_data="view_points"))
        #  InlineKeyboardButton(text="Удалить задание", callback_data="delete_menu"))
    keyboard_admin.add(
        InlineKeyboardButton(text="Назад", callback_data="control_script"))
    keyboard_admin.adjust(2, 2, repeat=True)
    return keyboard_admin.as_markup()


async def keyboard_create_point():
    keyboard_admin = InlineKeyboardBuilder()
    keyboard_admin.add(
        InlineKeyboardButton(text="Добавить задание", callback_data="add_point"),
        InlineKeyboardButton(text="Назад", callback_data="control_script"))
    keyboard_admin.adjust(2, 2, repeat=True)
    return keyboard_admin.as_markup()


async def keyboard_check_type_point():
    keyboard_admin = InlineKeyboardBuilder()
    keyboard_admin.add(
        InlineKeyboardButton(text="Да", callback_data=TypePoint(prefix="img", is_img=True).pack()),
        InlineKeyboardButton(text="Нет", callback_data=TypePoint(prefix="img", is_img=False).pack()))
    keyboard_admin.adjust(2, repeat=True)
    return keyboard_admin.as_markup()


async def delete_menu_key():
    keyboard_admin = InlineKeyboardBuilder()
    keyboard_admin.add(
        # InlineKeyboardButton(text="Удалить задание", callback_data="delete_menu")
        InlineKeyboardButton(text="В меню", callback_data="start_menu")
    )
    keyboard_admin.adjust(2, repeat=True)
    return keyboard_admin.as_markup()
