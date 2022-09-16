from aiogram.dispatcher.router import Router
from bot.filters.chat_type import ChatType
from .create_point import create_point_router
from .delete_point import delete_point_router
from .view_points import view_points_router

control_point_router = Router()
control_point_router.message.bind_filter(ChatType)

control_point_router.include_router(create_point_router)
control_point_router.include_router(delete_point_router)
control_point_router.include_router(view_points_router)
