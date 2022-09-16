from aiogram.filters import BaseFilter
from aiogram import types
from typing import Union, List
from bot.services.repo import SQLAlchemyRepo, GameRepo, PointRepo, ScriptRepo


class GameState(BaseFilter):
    game_state: int

    async def __call__(self, message: types.Message, repo: SQLAlchemyRepo) -> bool:
        current_state = await repo.get_repo(GameRepo).get_game_state()
        return current_state == self.game_state

