from aiogram.dispatcher.router import Router
from bot.filters.chat_type import ChatType
from magic_filter import F
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from bot.texts.private.control_game import tx_control_game
from bot.keyboards.private.control_game import kb_control_game
from bot.services.repo import SQLAlchemyRepo, ProtocolRepo
from bot.utils import export_protocol
from .control_game_panel import control_game


protocol_game_router = Router()
protocol_game_router.message.bind_filter(ChatType)


@protocol_game_router.callback_query(F.data == "get_protocol")
async def get_protocol(call: types.CallbackQuery, bot: Bot, repo: SQLAlchemyRepo):
    await call.answer()
    await call.message.delete()
    await call.message.answer(text=tx_control_game.PROTOCOL_TEXT,
                              reply_markup=await kb_control_game.protocol_menu(repo=repo))


@protocol_game_router.callback_query(F.data == "current_protocol")
async def get_current_protocol(call: types.CallbackQuery, bot: Bot, repo: SQLAlchemyRepo):
    await call.answer()
    await call.message.delete()
    await call.message.answer(text=await tx_control_game.get_current_protocol_text(repo=repo),
                              reply_markup=await kb_control_game.export_protocol_menu(type_protocol="current"))


@protocol_game_router.callback_query(F.data == "final_protocol")
async def get_final_protocol(call: types.CallbackQuery, bot: Bot, repo: SQLAlchemyRepo):
    await call.answer()
    await call.message.delete()
    await call.message.answer(text=await tx_control_game.get_final_protocol_text(repo=repo),
                              reply_markup=await kb_control_game.export_protocol_menu(type_protocol="final"))


@protocol_game_router.callback_query(F.data == "export_current_protocol")
async def export_current_protocol(call: types.CallbackQuery, bot: Bot, repo: SQLAlchemyRepo, state: FSMContext):
    await call.answer()
    name_file_protocol = await export_protocol.export_current_protocol(repo=repo)
    await call.message.answer_document(types.FSInputFile(name_file_protocol))
    await control_game(call=call, repo=repo, state=state)


@protocol_game_router.callback_query(F.data == "export_final_protocol")
async def export_final_protocol(call: types.CallbackQuery, bot: Bot, repo: SQLAlchemyRepo, state: FSMContext):
    await call.answer()
    name_file_protocol = await export_protocol.export_final_protocol(repo=repo)
    await call.message.answer_document(types.FSInputFile(name_file_protocol))
    await control_game(call=call, repo=repo, state=state)

