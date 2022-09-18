from aiogram.dispatcher.router import Router
from bot.filters.chat_type import ChatType
from magic_filter import F
from aiogram import types, Bot
from bot.services.repo import SQLAlchemyRepo, GameRepo, TeamRepo, ProtocolRepo, StateRepo
from aiogram.fsm.context import FSMContext
from bot.texts.private.control_game import tx_control_game
from bot.keyboards.private.control_game import kb_control_game
from .control_game_panel import control_game
from bot.utils.bot_leave import bot_leave
from bot.utils.drop_files import drop_files


reset_game_router = Router()
reset_game_router.message.bind_filter(ChatType)


@reset_game_router.callback_query(F.data.in_({"reset_game", "cancel_game"}))
async def stop_game(call: types.CallbackQuery, bot: Bot, repo: SQLAlchemyRepo, state: FSMContext):
    await call.answer()
    await bot_leave(bot=bot, repo=repo)
    await repo.get_repo(GameRepo).reset_game()
    await repo.get_repo(TeamRepo).reset_teams()
    await repo.get_repo(ProtocolRepo).reset_protocol()
    await repo.get_repo(StateRepo).reset_state()
    await drop_files()
    await control_game(call=call, repo=repo)
