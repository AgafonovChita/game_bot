import datetime
from bot.db.models import Endpoint
from bot.services.repo import SQLAlchemyRepo, StateRepo
from aiogram import Bot


ANSWER_CORRECT = f"\U0001F4A5 Отлично!\nВы нашли все коды на этом уровне!\nПродолжайте в том же духе!"

GAME_NOT_START = f"\U0000203C Игра находится в статусе запланированной и ещё не началась, " \
                 f"но вы делаете всё абсолютно правильно.\n\nКак только организатор начнут игру, " \
                 f"Вам придёт сообщение с первым заданием и я смогу принимать ответы."

ANSWER_IS_EMPTY = f"Ответ не может быть пустым сообщением\n\n" \
                  f"\U0000203C<b>Ответ</b> - это одно кодовое <u><b>слово</b></u>, состоящее <u><b>только</b></u> из " \
                  f"строчных букв кириллицы и/или цифр. "

ORGANIZER_STOPPED_GAME = f"\U0000203C Внимание\n" \
                         f"Организатор только что завершил игру.\n\n " \
                         f"Я больше не могу принимать от Вас ответы."

async def bot_instruction(bot: Bot):
    bot_info = await bot.get_me()
    return f"\U0001F929	Приветствую Вас, уважаемые игроки!\nМеня зовут {bot_info.first_name}\n" \
           f"Сегодня я буду руководить игрой: проверять ваши ответы и давать подсказки." \
           f"\n\nЧтобы проверить ответ Вам необходимо тегнуть меня и указать ваш вариант ответа.\n" \
           f"<b>Например:</b>\n<code>@{bot_info.username} чита75 </code>\n\n" \
           f"<b>\U0000203C Ответ</b> - это <u><b>одно</b></u> кодовое слово, состоящее <u><b>только</b></u> " \
           f"из строчных букв кириллицы и/или цифр.\n\n" \
           f"Как только организатор <b>начнёт игру</b>, вам сразу же придёт сообщение с первым заданием.\n\n" \
           f"<b>Удачи!</b>"


async def game_is_complete():
    """Игра завершена (либо команда прошла все уровни, либо организатор завершил игру) """
    return f"\U0001F3C1 \U0001F3C1 \U0001F3C1 \U0001F3C1 \U0001F3C1" \
           f"<b>Поздравляем!</b>\n\n" \
           f"Вы успешно <b>завершили</b> все этапы игры!\n\n" \
           f"\U0000231B Время финиша: <b>{datetime.datetime.now()}</b>"


async def organizer_stopped_game():
    return


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


async def point_help_text(point: Endpoint):
    return f"<b>\U0000203C ВНИМАНИЕ!\n" \
           f"Открыта подсказка!\n\n" \
           f"Уровень №{point.point_id}</b>\n\n{point.point_help_text}"



