from aiogram.dispatcher.router import Router
from bot.filters.chat_type import ChatType
from magic_filter import F
from aiogram import types
from bot.services.repo import SQLAlchemyRepo, GameRepo, ScriptRepo
from aiogram.fsm.context import FSMContext
from bot.texts.private.control_game import tx_control_game
from bot.keyboards.private.control_game import kb_control_game
from bot.keyboards.private.control_game.kb_control_game import DescriptionCallback, EditDescriptionCallback
from .control_game_panel import control_game
from bot.models.states import EditDescription


description_game_router = Router()
description_game_router.message.bind_filter(ChatType)


@description_game_router.callback_query(F.data == "description_game")
async def description_game(call: types.CallbackQuery, repo: SQLAlchemyRepo):
    await call.answer()
    await call.message.delete()
    await call.message.answer(text=tx_control_game.DESCRIPTION,
                              reply_markup=await kb_control_game.description_type())


@description_game_router.callback_query(DescriptionCallback.filter())
async def get_type_description(call: types.CallbackQuery, callback_data: DescriptionCallback, repo: SQLAlchemyRepo):
    await call.answer()
    await call.message.delete()
    await call.message.answer(text=await tx_control_game.get_description(repo=repo, type_d=callback_data.type),
                              reply_markup=await kb_control_game.edit_description(type_d=callback_data.type))


@description_game_router.callback_query(EditDescriptionCallback.filter())
async def edit_description_text(call: types.CallbackQuery, callback_data: EditDescriptionCallback, repo: SQLAlchemyRepo,
                                 state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer(text=await tx_control_game.enter_description_text(type_d=callback_data.type))
    await state.set_state(EditDescription.get_description_start
                          if callback_data.type == "start" else EditDescription.get_description_final)


@description_game_router.message(state=EditDescription.get_description_start)
async def get_text_description_start(message: types.Message, repo: SQLAlchemyRepo, state: FSMContext):
    game_idx = await repo.get_repo(ScriptRepo).get_script_id()
    await repo.get_repo(GameRepo).update_description_start(game_id=game_idx,
                                                           description_text=f"{await tx_control_game.description_title(type_d='start')}"
                                                                            f"<i>{message.text}</i>")
    await state.clear()
    await message.answer(text=tx_control_game.DESCRIPTION,
                         reply_markup=await kb_control_game.description_type())


@description_game_router.message(state=EditDescription.get_description_final)
async def get_text_description_final(message: types.Message, repo: SQLAlchemyRepo, state: FSMContext):
    game_idx = await repo.get_repo(ScriptRepo).get_script_id()
    await repo.get_repo(GameRepo).update_description_final(game_id=game_idx,
                                                           description_text=f"{await tx_control_game.description_title(type_d='final')}"
                                                                            f"<i>{message.text}</i>")

    await state.clear()
    await message.answer(text=tx_control_game.DESCRIPTION,
                         reply_markup=await kb_control_game.description_type())










