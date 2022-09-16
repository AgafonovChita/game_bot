from aiogram.filters import BaseFilter
from aiogram import types
from typing import Union, List


class ChatType(BaseFilter):
    chat_type: Union[str, List[str]]

    async def __call__(self, obj: Union[types.Message, types.CallbackQuery, types.ChatMemberUpdated]) -> bool:
        if isinstance(obj, types.Message):
            chat_type = obj.chat.type
        elif isinstance(obj, types.CallbackQuery):
            chat_type = obj.message.chat.type if obj.message else None
        elif isinstance(obj, types.ChatMemberUpdated):
            chat_type = obj.chat.type

        return chat_type in self.chat_type
