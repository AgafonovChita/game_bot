from aiogram import types, Bot
from magic_filter import F
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext

from bot.keyboards.private.control_script import kb_base
from bot.keyboards.private.control_script import kb_control_point
from bot.texts.private.control_script.control_point import tx_delete_point, tx_control_point
from bot.services.repo.base_repo import SQLAlchemyRepo
from bot.models.states import DeletePoint
from bot.services.repo import PointRepo
from bot.keyboards.private.control_script.kb_base import DeleteCallback

delete_point_router = Router()


@delete_point_router.callback_query(F.data == "delete_menu")
async def delete_point_menu(call: types.CallbackQuery, repo: SQLAlchemyRepo, state: FSMContext):
    await call.answer()
    await call.message.answer(text=tx_delete_point.delete_point_get_id)
    await state.set_state(DeletePoint.get_id_point)


@delete_point_router.message(state=DeletePoint.get_id_point)
async def delete_point_check(message: types.Message, repo: SQLAlchemyRepo, state: FSMContext):
    await state.update_data(id_point=message.text)
    check = await repo.get_repo(PointRepo).check_point(point_id=message.text)
    if check:
        await message.answer(text=await tx_control_point.get_point(repo=repo, point_id=message.text),
                             reply_markup=await kb_base.delete_check_key())
        await state.set_state(DeletePoint.delete_point)
        return
    await message.answer(text=await tx_delete_point.point_is_not_found(repo=repo),
                         reply_markup=await kb_control_point.delete_menu_key())


@delete_point_router.callback_query(DeleteCallback.filter(F.check), state=DeletePoint.delete_point)
async def delete_point(call: types.CallbackQuery, repo: SQLAlchemyRepo, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await call.message.delete()
    await repo.get_repo(PointRepo).delete_point(point_id=data.get("id_point"))
    await call.message.answer(text=await tx_delete_point.point_is_deleted(repo=repo),
                              reply_markup=await kb_control_point.keyboard_control_point(repo=repo))


@delete_point_router.callback_query(DeleteCallback.filter(F.check.is_(False)), state=DeletePoint.delete_point)
async def not_delete_point(call: types.CallbackQuery, bot: Bot, repo: SQLAlchemyRepo):
    await call.answer()
    await call.message.delete()
    await call.message.answer(text=await tx_control_point.edit_script(repo=repo),
                              reply_markup=await kb_control_point.keyboard_control_point(repo=repo))



