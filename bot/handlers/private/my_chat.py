from aiogram import types, Bot
from aiogram.dispatcher.router import Router

from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram.methods import LeaveChat

import bot.engine.description_api
from bot.services.repo.base_repo import SQLAlchemyRepo
from bot.services.repo import TeamRepo
from bot.filters import GameState, ChatType
from bot.engine import description_api

my_chat_router = Router()
my_chat_router.my_chat_member.bind_filter(GameState)
my_chat_router.my_chat_member.bind_filter(ChatType)


@my_chat_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
                               game_state=1, chat_type=["group", "supergroup"])
async def bot_added(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """Бот был добавлен в групповой чат одной из команд"""
    await repo.get_repo(TeamRepo).add_team(team_id=update.chat.id,
                                           team_name=update.chat.title,
                                           captain_username=update.from_user.username
                                           if update.from_user.username else "NotUserName")

    await description_api.send_bot_instruction(team_id=update.chat.id, bot=bot)

    await description_api.send_description_start(team_id=update.chat.id,
                                                            bot=bot,
                                                            repo=repo)



@my_chat_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION),
                               game_state=1, chat_type=["group", "supergroup"])
async def bot_leave(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo):
    """Бот был удалён из чата одной из команд"""
    await repo.get_repo(TeamRepo).delete_team(team_idx=update.chat.id)



@my_chat_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def bot_added(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo):
    """Если бота добавили вне запланированной игры - бот выходит из чата"""
    await LeaveChat(chat_id=update.chat.id)



