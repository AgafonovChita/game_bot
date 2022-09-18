from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData


GAME_STATES = {None: " не запланирована \U0000274C", 1: " запланирована \U000023F3",
               2: " игра активна \U000026A1", 3: " игра завершена \U0000274E"}


class CreateGame(StatesGroup):
    name_game = State()


class CreatePoint(StatesGroup):
    point_text = State()
    point_is_img = State()
    point_get_id_img = State()
    point_answer = State()
    point_help_text_is_img = State()
    point_help_text_id_img = State()
    point_help_text = State()
    point_get_timeout = State()


class DeletePoint(StatesGroup):
    get_id_point = State()
    delete_point = State()


class DeleteScript(StatesGroup):
    delete_script = State()


class EditDescription(StatesGroup):
    get_description_start = State()
    get_description_final = State()
