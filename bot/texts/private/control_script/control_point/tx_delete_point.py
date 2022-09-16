from bot.services.repo import SQLAlchemyRepo, PointRepo, ScriptRepo
from bot.texts.private import tx_base

delete_point_get_id = f"Введите ID задания, который желаете удалить\n\n" \
                      f"Узнать ID нужного задания можно через меню 'Просмотреть задание'"


async def point_is_deleted(repo: SQLAlchemyRepo):
    return f"Задание успешно удалено\n\n" \
           f"{await tx_base.get_description_script(repo=repo)}"


async def point_is_not_found(repo: SQLAlchemyRepo):
    return f"Задание c таким ID не обнаружено в базе данных\n\n" \
           f"{await tx_base.get_description_script(repo=repo)}"
