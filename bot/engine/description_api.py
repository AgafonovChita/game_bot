from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from bot.services.repo import SQLAlchemyRepo, GameRepo
from bot.texts.game_engine import tx_game_engine


async def send_description_start(team_id: int, repo: SQLAlchemyRepo, bot: Bot):
    description_start = await repo.get_repo(GameRepo).get_description_start()
    try:
        await bot.send_message(chat_id=team_id,
                               text=description_start)
    except TelegramBadRequest:
        pass


async def send_bot_instruction(team_id: int, bot: Bot):
    try:
        await bot.send_message(chat_id=team_id,
                               text=await tx_game_engine.bot_instruction(bot=bot))
    except TelegramBadRequest:
        pass


async def send_description_final(team_id: int, bot: Bot, repo: SQLAlchemyRepo):
    description_final = await repo.get_repo(GameRepo).get_description_final()
    try:
        await bot.send_message(chat_id=team_id,
                               text=description_final)
    except TelegramBadRequest:
        pass


async def send_description_stop_game(team_id: int, bot: Bot):
    try:
        await bot.send_message(chat_id=team_id,
                               text=tx_game_engine.ORGANIZER_STOPPED_GAME)
    except TelegramBadRequest:
        pass

