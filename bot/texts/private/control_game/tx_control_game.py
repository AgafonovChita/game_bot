import datetime
from aiogram import Bot
from bot.services.repo import SQLAlchemyRepo, GameRepo, TeamRepo, ProtocolRepo

IS_NOT_SCHEDULE = "Проведение игры разделено на 2 этапа\n\n" \
                  "<b>\U0001F539 Этап №1.</b> <i>Заранее перед игрой</i>\n" \
                  "Необходимо <b>ЗАПЛАНИРОВАТЬ ИГРУ</b>\n" \
                  "<i>C этого момента команды могут добавлять бота в свои групповые чаты. " \
                  "При добавлении бота командам будет приходить сообщение с инструкцией по работе с ботом.</i>\n\n" \
                  "<b>\U0001F539 Этап №2.</b> <i>Когда все команды готовы.</i>\n" \
                  "Дать <b>СТАРТ ИГРЕ</b>\n" \
                  "<i>Во все чаты, куда был добавлен бот будет отправлено первое задание, " \
                  "бот начнёт принимать ответы, давать подсказки и фиксировать время прохождения</i>"

IS_SCHEDULE = "<b>\U0000203C Проведение игры ЗАПЛАНИРОВАНО</b>\n\n" \
              "<i>C этого момента команды могут начать добавлять бота в свои групповые чаты. " \
              "При добавлении бота командам будет приходить сообщение с инструкцией по работе с ботом.</i>\n\n" \
              "<b>\U0001F539 Этап №2.</b> <i>Когда все команды готовы.</i>\n" \
              "Дать <b>СТАРТ ИГРЕ</b>\n" \
              "<i>Во все чаты, куда был добавлен бот будет отправлено первое задание, " \
              "бот начнёт принимать ответы, давать подсказки и фиксировать время прохождения</i>"

IS_START = "<b>\U000026A1 ИГРА ЗАПУЩЕНА \n\n </b>" \
           "<i>Вы можете следить за статистикой в меню <b>ПРОТОКОЛ</b></i>"

IS_COMPLETE = "<b>\U0000274E ИГРА БЫЛА ЗАВЕРШЕНА </b> \n\n" \
              "<i>Вы можете просмотреть/скачать протокол игры. \n\nЕсли вы желаете запланировать новую игру," \
              "вам необходимо <b>сбросить данные</b>. После сброса данных, текущий протокол будет удалён и " \
              "вы сможете запланировать проведение новой игры.</i>"

PROTOCOL_TEXT = f"Поддерживается 2 формы протокола:\n\n" \
                f"<b>\U0001F4C8 Текущий протокол</b> - <i>информация о точках, пройденных командами на текущий момент.</i>\n\n" \
                f"<b>\U0001F4CA Итоговый протокол</b> - <i>финальное распределение мест по итогам игры. Итоговый протокол " \
                f"доступен только после того, как игра будет завершена.</i>"

CANCEL_GAME = f"Отмена запланированной игры приведёт к сбросу состояний игры.\n\n" \
              f"<b>Внимание!</b>\n<i>Бот покинет все групповые " \
              f"чаты, в которые уже был добавлен командами ранее. При новом планировании игры " \
              f"командам необходимо будет снова добавить бота в групповые чаты. </i>"

DESCRIPTION_START = f"\U000025B6 <b>Стартовая инструкция:</b>\n" \
                    f"<i>Команды получат эту инструкцию сразу после того, как добавят бота себе в групповой чат</i>\n\n"

DESCRIPTION_FINAL = f"<b>\U0001F3C1 Финальная инструкция:</b> \n" \
                    f"<i>Команды получат эту инструкцию сразу после того, как закроют последний уровень, " \
                    f"либо после того, как администратор <b>завершит игру</b></i>"

DESCRIPTION = f"{DESCRIPTION_START}\n{DESCRIPTION_FINAL}"


async def enter_description_text(type_d: str):
    return f"Введите текст для {'стартовой' if type_d == 'start' else 'финальной'} инструкции\n\n" \
           f"{DESCRIPTION_START if type_d == 'start' else DESCRIPTION_FINAL}"


async def control_game_text(repo: SQLAlchemyRepo):
    game_state = await repo.get_repo(GameRepo).get_game_state()
    if game_state is None:
        return IS_NOT_SCHEDULE
    elif game_state == 1:
        return IS_SCHEDULE
    elif game_state == 2:
        return IS_START
    elif game_state == 3:
        return IS_COMPLETE


async def stop_game_text(repo: SQLAlchemyRepo):
    # statistics = await repo.get_repo(ProtocolRepo).get_statistics()
    return f"\U00002757 ВНИМАНИЕ\nПосле подтверждения продолжение игры будет невозможно\n\n" \
           f"<i>Команды больше не будут получать задания и не смогут вводить ответы. " \
           f"Протокол игры будет зафиксирован в текущем состоянии.</i>"


async def teams_text(repo: SQLAlchemyRepo):
    teams = await repo.get_repo(TeamRepo).get_teams_list()
    text = f"\U0001F4CB Список команд, <b>зарегистрированных</b> на игру.\n\n" \
           f"<i>Чтобы команда получила доступ к игровому движку, команде необходимо создать групповой чат, " \
           f"назвать чат в соответствии с названием своей команды и добавить в чат бота @game_travel_bot</i>\n\n"
    if teams:
        for idx, team in enumerate(teams, start=1):
            text += f"<b>{idx}.</b> Команда: <i>{team.team_name}</i>\n" \
                    f"<b>Капитан:</b> <i>@{team.team_captain_username}</i>\n\n"
    return text


async def get_current_protocol_text(repo: SQLAlchemyRepo):
    current_protocol_list = await repo.get_repo(ProtocolRepo).get_current_protocol_list()
    text = f"<b>Текущий протокол на:</b> \n<i>{datetime.datetime.now()}</i>\n\n"
    for protocol in current_protocol_list:
        text += f"\U0001F538 <b>Команда:</b> <i>{protocol.team_name}\n</i>" \
                f"\U00002705 <b>Последняя точка:</b> <i>{protocol.point_id}\n</i>" \
                f"\U0001F55B <b>Когда взяли:</b> <i>{protocol.point_close_time}\n\n</i>"
    return text


async def get_final_protocol_text(repo: SQLAlchemyRepo):
    final_protocol_list = await repo.get_repo(ProtocolRepo).get_final_protocol_to_export()
    text = f"<b>Итоговый протокол</b>\n\n"
    for idx, protocol in enumerate(final_protocol_list, start=1):
        text += f"<b>{idx} место\n</b>" \
                f"\U0001F538 Команда: {protocol.team_name}\n" \
                f"\U00002705 Финальная точка: {protocol.point_id}\n" \
                f"\U0001F55B Финишное время: {protocol.finish_time}\n\n"
    return text

async def description_title(type_d: str):
    title = "\U0001F4E3 Стартовая инструкция\n\n" if type_d == "start" else "\U0001F3C1 Финальная инструкция\n\n"
    return f"\U0000203C	Внимание\n\n" \
           f"{title}" \
           f"Ознакомьтесь с инструкцией, предоставленной организатором игры. Будьте " \
           f"предельно внимательны, каждая деталь может оказаться важна.\n\n "
async def get_description(repo: SQLAlchemyRepo, type_d: str):
    description = await repo.get_repo(GameRepo).get_description_start() \
        if type_d == "start" else await repo.get_repo(GameRepo).get_description_final()
    return f"{description}"




