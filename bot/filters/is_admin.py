from aiogram.filters import BaseFilter
from aiogram import types

from typing import Union, List
from bot.config import admins
from aiogram.methods.get_chat_member import GetChatMember


class IsAdmin(BaseFilter):
    is_admin: bool

    async def __call__(self, message: types.Message) -> bool:
        user_id = message.from_user.id
        return user_id in admins
