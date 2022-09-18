from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from bot.services.repo import GameRepo, SQLAlchemyRepo, ProtocolRepo


class CompleteCallback(CallbackData, prefix="complete"):
    check: bool

class DescriptionCallback(CallbackData, prefix="description"):
    type: str

class EditDescriptionCallback(CallbackData, prefix="edit_description"):
    type: str


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
        keyboard.add(InlineKeyboardButton(text="\U0001F4C5 Запланировать игру", callback_data="schedule_game"))
    elif game_state == 1:
        keyboard.add(InlineKeyboardButton(text="\U000025B6 Начать игру", callback_data="start_game"),
                     InlineKeyboardButton(text="\U0001F51A Отменить игру", callback_data="check_cancel_game"),
                     InlineKeyboardButton(text="\U0001F5D2 Список команд", callback_data="get_teams"),
                     InlineKeyboardButton(text="\U0001F4DD Инструкции по игре", callback_data="description_game"))
    elif game_state == 2:
        keyboard.add(
            InlineKeyboardButton(text="\U0001F4CB Протокол", callback_data="get_protocol"),
            InlineKeyboardButton(text="\U000023F9 Завершить игру", callback_data="stop_game"))

    elif game_state == 3:
        keyboard.add(InlineKeyboardButton(text="\U0001F4CB Протокол", callback_data="get_protocol"),
                     InlineKeyboardButton(text="\U0000267B Сбросить данные", callback_data="reset_game"))

    keyboard.add(
        InlineKeyboardButton(text="\U000021AA В меню", callback_data="start_menu"))
    keyboard.adjust(2, 2, repeat=True)
    return keyboard.as_markup()


async def return_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="\U0001F503 Обновить", callback_data="get_teams"),
        InlineKeyboardButton(text="\U000021AA В меню", callback_data="control_game"))
    keyboard.adjust(2, 2, repeat=True)
    return keyboard.as_markup()


async def description_type():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="\U000025B6 Стартовая инструкция",
                             callback_data=DescriptionCallback(type="start").pack()),
        InlineKeyboardButton(text="\U0001F3C1 Финальная инструкция",
                             callback_data=DescriptionCallback(type="final").pack()),
        InlineKeyboardButton(text="\U000021AA В меню", callback_data="control_game"))
    keyboard.adjust(2, 2, repeat=True)
    return keyboard.as_markup()


async def edit_description(type_d: str):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="\U0001F4D1 Изменить инструкцию",
                             callback_data=EditDescriptionCallback(type=type_d).pack()),
        InlineKeyboardButton(text="\U000021AA В меню", callback_data="description_game"))
    keyboard.adjust(2, 2, repeat=True)
    return keyboard.as_markup()


async def check_cancel_game():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="\U0001F51A Отменить игру", callback_data="cancel_game"),
        InlineKeyboardButton(text="\U000021AA В меню", callback_data="control_game"))
    keyboard.adjust(2, 2, repeat=True)
    return keyboard.as_markup()


async def teams_list():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="\U000021AA В меню", callback_data="control_game"))
    keyboard.adjust(2, 2, repeat=True)
    return keyboard.as_markup()


async def export_protocol_menu(type_protocol: str):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="\U0001F4BE Экспорт",
                             callback_data="export_final_protocol"
                             if type_protocol == "final" else "export_current_protocol"),
        InlineKeyboardButton(text="\U000021AA В меню", callback_data="control_game"))
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
