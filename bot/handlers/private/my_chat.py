from aiogram import types
from aiogram.dispatcher.router import Router

from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.filters import JOIN_TRANSITION
from aiogram.methods import LeaveChat
from bot.services.repo.base_repo import SQLAlchemyRepo
from bot.services.repo import TeamRepo
from bot.filters import GameState, ChatType

my_chat_router = Router()
my_chat_router.my_chat_member.bind_filter(GameState)
my_chat_router.my_chat_member.bind_filter(ChatType)


@my_chat_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
                               game_state=1, chat_type=["group", "supergroup"])
async def bot_added(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo):
    """Бот был добавлен в групповой чат одной из команд"""
    await repo.get_repo(TeamRepo).add_team(team_id=update.chat.id,
                                           team_name=update.chat.title,
                                           captain_username=update.from_user.username
                                           if update.from_user.username else "NotUserName")


@my_chat_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def bot_added(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo):
    """Если бота добавили вне запланированной игры - бот выходит из чата"""
    await LeaveChat(chat_id=update.chat.id)



