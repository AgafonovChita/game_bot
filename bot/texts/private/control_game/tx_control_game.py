import datetime

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
    #statistics = await repo.get_repo(ProtocolRepo).get_statistics()
    return f"\U00002757 ВНИМАНИЕ\nПосле подтверждения продолжение игры будет невозможно\n\n" \
           f"<i>Команды больше не будут получать задания и не смогут вводить ответы. " \
           f"Протокол игры будет зафиксирован в текущем состоянии.</i>"


async def teams_text(repo: SQLAlchemyRepo):
    teams = await repo.get_repo(TeamRepo).get_teams_list()
    text = ''
    if teams:
        for idx, team in enumerate(teams, start=1):
            text += f"{idx}: {team.team_name}\n"
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
        text += f"{idx} место\n" \
                f"Команда: {protocol.team_name}\n" \
                f"Финальная точка: {protocol.point_id}" \
                f"Финишное время: {protocol.point_close_time}"
    return text

