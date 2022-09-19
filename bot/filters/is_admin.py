from aiogram.filters import BaseFilter
from aiogram import types

from config_reader import config


class IsAdmin(BaseFilter):
    is_admin: bool

    async def __call__(self, message: types.Message) -> bool:
        user_id = message.from_user.id
        return user_id in config.admin_ids
