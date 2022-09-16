from aiogram import types, Bot
from aiogram.filters.content_types import ContentType, ContentTypesFilter
from aiogram.fsm.context import FSMContext
from magic_filter import F

from aiogram.dispatcher.router import Router

from bot.keyboards.private.control_script import kb_control_point
from bot.texts.private.control_script.control_point import tx_create_point
from bot.filters.chat_type import ChatType

from bot.services.repo.base_repo import SQLAlchemyRepo
from bot.services.repo import PointRepo

from bot.keyboards.private.control_script.kb_control_point import TypePoint
from bot.models.states import CreatePoint

create_point_router = Router()
create_point_router.message.bind_filter(ChatType)


@create_point_router.callback_query(F.data == "add_point")
async def add_point(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    """Создать новое задание"""
    await call.answer()
    await call.message.answer(tx_create_point.print_text_point)

    await state.set_state(CreatePoint.point_text)


@create_point_router.message(state=CreatePoint.point_text)
async def get_text_point(message: types.Message, bot: Bot, state: FSMContext):
    """Записываем текст задания"""
    await state.update_data(text_point=message.text.lower())
    await bot.delete_message(chat_id=message.chat.id,  message_id=message.message_id - 1)
    await message.answer(text=tx_create_point.text_point_is_img,
                         reply_markup=await kb_control_point.keyboard_check_type_point())
    await state.set_state(CreatePoint.point_is_img)


@create_point_router.callback_query(TypePoint.filter(F.is_img), state=CreatePoint.point_is_img)
async def is_img(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    """Если задание содержит изображение - просим пользователя его отправить"""
    await call.answer()
    await call.message.answer(tx_create_point.print_id_img)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.set_state(CreatePoint.point_get_id_img)


@create_point_router.message(ContentTypesFilter(content_types=[ContentType.PHOTO]), state=CreatePoint.point_get_id_img)
async def get_id_img(message: types.Message, bot: Bot, state: FSMContext):
    """Принимаем изображение, сохраняем его id"""
    await state.update_data(point_is_img=True, point_img_id=message.photo[-1].file_id)
    await message.answer(tx_create_point.get_answers_text)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await state.set_state(CreatePoint.point_answer)


@create_point_router.callback_query(TypePoint.filter(F.is_img.is_(False)), state=CreatePoint.point_is_img)
async def is_not_img(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    """Задание не содержит изображения"""
    await call.answer()
    await state.update_data(point_is_img=False)
    await call.message.answer(tx_create_point.get_answers_text)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.set_state(CreatePoint.point_answer)


@create_point_router.message(state=CreatePoint.point_answer)
async def get_answers(message: types.Message, bot: Bot, state: FSMContext):
    """Сохраняем коды(ответы)"""
    await state.update_data(answers=message.text)
    await message.answer(tx_create_point.help_text)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await state.set_state(CreatePoint.point_help_text)


@create_point_router.message(state=CreatePoint.point_help_text)
async def get_help_text(message: types.Message, bot: Bot, state: FSMContext):
    """Принимаем текст подсказки"""
    await state.update_data(help_text=message.text)
    await message.answer(tx_create_point.help_is_img,
                         reply_markup=await kb_control_point.keyboard_check_type_point())
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await state.set_state(CreatePoint.point_help_text_is_img)


@create_point_router.callback_query(TypePoint.filter(F.is_img), state=CreatePoint.point_help_text_is_img)
async def help_text_is_img(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    """Подсказка содержит изображение?"""
    await call.answer()
    await call.message.answer(tx_create_point.print_id_img)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.set_state(CreatePoint.point_help_text_id_img)


@create_point_router.message(ContentTypesFilter(content_types=[ContentType.PHOTO]), state=CreatePoint.point_help_text_id_img)
async def get_id_img_for_help(message: types.Message, bot: Bot, state: FSMContext):
    """Принимаем изображение, сохраняем его id"""
    await state.update_data(point_help_text_is_img=True, point_help_text_img_id=message.photo[-1].file_id)
    await message.answer(tx_create_point.help_timeout)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await state.set_state(CreatePoint.point_get_timeout)


@create_point_router.callback_query(TypePoint.filter(F.is_img.is_(False)), state=CreatePoint.point_help_text_is_img)
async def description_is_not_img(call: types.CallbackQuery, bot: Bot,  state: FSMContext):
    """Подсказка не содержит изображения"""
    await call.answer()
    await state.update_data(point_help_text_is_img=False)
    await call.message.answer(tx_create_point.help_timeout)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.set_state(CreatePoint.point_get_timeout)


@create_point_router.message(state=CreatePoint.point_get_timeout)
async def get_timeout(message: types.Message, state: FSMContext, bot: Bot, repo: SQLAlchemyRepo):
    await state.update_data(timeout=message.text)
    data = await state.get_data()
    await repo.get_repo(PointRepo).add_point(point=data)

    await message.answer(await tx_create_point.point_is_added(repo=repo),
                         reply_markup=await kb_control_point.keyboard_control_point(repo=repo))
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await state.clear()

