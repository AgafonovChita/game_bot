from aiogram.filters import BaseFilter
from aiogram import types
from aiogram import Bot


class TagBot(BaseFilter):
    tag_bot: bool

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        bot_info = await bot.get_me()
        status = message.entities and message.entities[0].type == 'mention' and bot_info.username in message.text
        return status == self.tag_bot
