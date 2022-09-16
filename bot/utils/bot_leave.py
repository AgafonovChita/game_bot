from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from bot.services.repo import SQLAlchemyRepo, TeamRepo

async def bot_leave(bot: Bot, repo:SQLAlchemyRepo):
    teams = await repo.get_repo(TeamRepo).get_teams_list()
    for team in teams:
        try:
            await bot.leave_chat(chat_id=team.team_id)
        except TelegramBadRequest:
            pass

