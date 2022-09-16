import asyncio
from aiogram import Bot
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup


async def send_message(text: str, ids: list[int], bot: Bot, markup: InlineKeyboardMarkup = None):
    print(type(markup))
    for idx in ids:
        try:
            await bot.send_message(chat_id=idx,
                                   text=text,
                                   reply_markup=markup)
        except Exception as e:
            pass

        finally:
            await asyncio.sleep(0.03)


async def send_question(text: str, idx: int, bot: Bot):
    await bot.send_message(chat_id=idx, text=text)
