from bot.services.repo import SQLAlchemyRepo, PointRepo, ScriptRepo

from bot.texts.private import tx_base

create_script = f"Введите название/описание для сценария, который хотите создать.\n\n" \
                f"<i>Это может быть предполагаемая дата игры и небольшое описание</i>"


async def script_is_creating(name_game: str, repo: SQLAlchemyRepo):
    return f"Сценарий <b>{name_game}</b> успешно создан\n\n" \
           f"{await tx_base.get_description_script(repo=repo)}"



