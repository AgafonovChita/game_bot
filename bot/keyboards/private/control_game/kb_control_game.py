from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from bot.services.repo import GameRepo, SQLAlchemyRepo, ProtocolRepo


class CompleteCallback(CallbackData, prefix="complete"):
    check: bool


async def stop_game():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Завершить", callback_data=CompleteCallback(check=True).pack()),
        InlineKeyboardButton(text="Отмена", callback_data=CompleteCallback(check=False).pack()))
    keyboard.adjust(2, repeat=True)
    return keyboard.as_markup()

async def keyboard_control_game_panel(repo: SQLAlchemyRepo):
    keyboard = InlineKeyboardBuilder()
    game_state = await repo.get_repo(GameRepo).get_game_state()
    if game_state is None:
        keyboard.add(InlineKeyboardButton(text="Запланировать игру", callback_data="schedule_game"))
    elif game_state == 1:
        keyboard.add(InlineKeyboardButton(text="Начать игру", callback_data="start_game"),
                     InlineKeyboardButton(text="Отменить игру", callback_data="start_game"),
                     InlineKeyboardButton(text="Команды", callback_data="get_teams"))
    elif game_state == 2:
        keyboard.add(InlineKeyboardButton(text="Завершить игру", callback_data="stop_game"))

    elif game_state == 3:
        keyboard.add(InlineKeyboardButton(text="Сбросить данные", callback_data="reset_game"))

    keyboard.add(
        InlineKeyboardButton(text="Протокол", callback_data="get_protocol"),
        InlineKeyboardButton(text="В меню", callback_data="start_menu"))
    keyboard.adjust(2, 2, repeat=True)
    return keyboard.as_markup()


async def return_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="В меню", callback_data="control_game"))
    keyboard.adjust(2, 2, repeat=True)
    return keyboard.as_markup()


async def export_protocol_menu(type_protocol: str):
    keyboard = InlineKeyboardBuilder()
    if type_protocol == "final":
        keyboard.add(
            InlineKeyboardButton(text="Экспорт", callback_data="export_final_protocol"))
    elif type_protocol == "current":
        keyboard.add(
            InlineKeyboardButton(text="Экспорт", callback_data="export_current_protocol"))
    keyboard.add(
       InlineKeyboardButton(text="В меню", callback_data="control_game"))
    keyboard.adjust(2, 2, repeat=True)
    return keyboard.as_markup()



async def protocol_menu(repo: SQLAlchemyRepo):
    game_state = await repo.get_repo(GameRepo).get_game_state()

    keyboard = InlineKeyboardBuilder()
    if game_state == 3:
        keyboard.add(
            InlineKeyboardButton(text="\U0001F4CA Итоговый протокол", callback_data="final_protocol"))
    keyboard.add(
        InlineKeyboardButton(text="\U0001F4C8 Текущий протокол", callback_data="current_protocol"),
        InlineKeyboardButton(text="\U000021AA В меню", callback_data="control_game"))
    keyboard.adjust(2, 2, repeat=True)
    return keyboard.as_markup()

