import datetime
from bot.db.models import Endpoint
from bot.services.repo import SQLAlchemyRepo, StateRepo

start_message = f"Приветствую Вас на Голодных играх, дети мои!\n\n" \
                "Сегодня я буду руководить игрой: проверять ваши ответы и давать подсказки." \
                "\n\nЧтобы проверить ответ Вам необходимо тегнуть меня и указать ваш вариант ответа.\n" \
                "<b>Например: </b> <code> @game_travel_bot улица Ленина </code>"


answer_correct = f"\U0001F4A5 Отлично!\nВы нашли все коды на этом уровне!\nПродолжайте в том же духе!"



async def game_is_complete():
    return f"\U0001F3C1 \U0001F3C1 \U0001F3C1 \U0001F3C1 \U0001F3C1" \
           f"<b>Поздравляем!</b>\n\n" \
           f"Вы успешно <b>завершили</b> все этапы игры!\n\n" \
           f"\U0000231B Время финиша: <b>{datetime.datetime.now()}</b>"


async def get_answer_text(team_idx: int, answer_status: str, repo: SQLAlchemyRepo):
    if answer_status == "ok":
        return f"\U00002705 Ответ принят\n\n{await get_current_answer(team_idx=team_idx, repo=repo)}"
    elif answer_status == "repeat":
        return f"\U00002B55 Вы уже давали этот ответ ранее\n\n{await get_current_answer(team_idx=team_idx, repo=repo)}"
    elif answer_status == "not_ok":
        return f"\U0000274C Это неверный ответ\n\n{await get_current_answer(team_idx=team_idx, repo=repo)}"

async def get_current_answer(team_idx: int, repo: SQLAlchemyRepo):
    current_answer = await repo.get_repo(StateRepo).get_current_answer(team_idx=team_idx)
    current_count = await repo.get_repo(StateRepo).get_current_count(team_idx=team_idx)
    correct_count = await repo.get_repo(StateRepo).get_correct_count(team_idx=team_idx)

    return f"<b>Прогресс:</b> <b>{current_count}/{correct_count} </b> кодов на этом уровне\n\n" \
           f"<b>Засчитанные коды:</b> <i>{current_answer}</i>"


async def point_description(point: Endpoint):
    return f"<b>Уровень №{point.point_id}</b>\n\n{point.point_text}"



