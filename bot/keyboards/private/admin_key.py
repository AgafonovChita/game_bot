from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.services.repo import SQLAlchemyRepo, GameRepo, PointRepo
from bot.models.states import GAME_STATES


async def keyboard_admin_panel(repo: SQLAlchemyRepo):
    keyboard_admin = InlineKeyboardBuilder()
    count_point = await repo.get_repo(PointRepo).get_count_point()
    game_state = await repo.get_repo(GameRepo).get_game_state()
    if count_point:
        keyboard_admin.add(
            InlineKeyboardButton(text=f"\U0001F538 Управление игрой - "
                                      f"{GAME_STATES.get(await repo.get_repo(GameRepo).get_game_state())}",
                                 callback_data="control_game"))
    if game_state is None:
        keyboard_admin.add(
            InlineKeyboardButton(text="\U0001F4C3 Управление сценарием",
                                 callback_data="control_script"))
    keyboard_admin.adjust(1, 1, repeat=True)
    return keyboard_admin.as_markup()
