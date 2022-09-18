from bot.services.repo import SQLAlchemyRepo, PointRepo, ScriptRepo

print_text_point = f"\U0001F5D2	Введите текст задания или описание к изображению, которое можно прикрепить позже"

text_point_is_img = f"\U0001F4F8 Задание содержит изображение?"

print_id_img = f"\U0001F4CE Прикрепите изображение как картинку (не как файл) и отправьте боту"

get_answers_text = f"\U0001F510 Введите коды(ответы) последовательно разделяя пробелом \n\n" \
                   f"<b>Например:</b> <code>3В Chita 75rus</code>"

help_text = f"\U0001F5E8 Введите подсказку к заданию или уточнение к изображению, которое можно прикрепить позже"

help_is_img = f"\U0001F4F8 Подсказка содержит изображение?"

help_timeout = f"\U0000231B	Введите таймаут для подсказки.\n\n" \
               "<i>Время в секундах, по прошествию которого игроки увидят подсказку. Отправить" \
               "необходимо <u><b>целое число</b></u> без указания единиц измерения</i>\n\n" \
               "<b>Например:</b> <code>60 </code>"


async def point_is_added(repo: SQLAlchemyRepo):
    count_point = await repo.get_repo(PointRepo).get_count_point()
    game = await repo.get_repo(ScriptRepo).get_script()
    return f"Задание успешно добавлено\n\n" \
           f"<b>Текущий сценарий: </b><i>{game.script_id} : {game.script_name}</i>\n" \
           f"<b>Количество заданий: </b><i>{count_point}</i>"
