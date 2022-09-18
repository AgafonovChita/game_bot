from aiogram import Bot


async def parse_answer(text: str):
    return text[text.index(" ")+1:]


async def answer_is_valid(text: str, bot: Bot):
    bot_info = await bot.get_me()
    return len(text) > len(bot_info.username)+1
