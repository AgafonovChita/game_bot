from bot.services.repo import SQLAlchemyRepo, PointRepo, ScriptRepo
from bot.db.models import Endpoint

script_is_not_found = f"В базе данных отсутствует сохранённый сценарий.\n\n" \
                      f"Создайте новый сценарий и заполните задания."


async def get_description_script(repo: SQLAlchemyRepo):
    count_point = await repo.get_repo(PointRepo).get_count_point()
    game = await repo.get_repo(ScriptRepo).get_script()
    if game:
        return f"<b>Текущий сценарий: </b><i>{game.script_id} : {game.script_name}</i>\n" \
                f"<b>Количество заданий: </b><i>{count_point}</i>"
    return script_is_not_found


async def get_formatted_point(point: Endpoint):
    return f"\U0001F538 id: {point.point_id}\n" \
           f"\U00002753 Текст: {point.point_text}\n" \
           f"\U0001F517 Подсказка: {point.point_help_text}\n" \
           f"\U0001F513 Коды: {point.point_answers}\n"