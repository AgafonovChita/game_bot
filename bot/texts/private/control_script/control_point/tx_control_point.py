from bot.services.repo import SQLAlchemyRepo, PointRepo, ScriptRepo
from bot.texts.private import tx_base


async def get_point(repo: SQLAlchemyRepo, point_id: int):
    point = await repo.get_repo(PointRepo).get_point(point_id=point_id)
    return f"{await tx_base.get_formatted_point(point)}\n" \
           f"<b>\U000023EC Подтвердите удаление задания \U000023EC</b>"


async def get_list_points(repo: SQLAlchemyRepo):
    list_points = await repo.get_repo(PointRepo).get_points_list()
    text = ''
    for point in list_points:
        text += f"{await tx_base.get_formatted_point(point)}" \
                f"___________\n\n"
    return text
