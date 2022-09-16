from bot.utils.sending import send_message
from aiogram import Bot
from bot.keyboards.game_engine.game_keyboards import generate_help_key
from bot.services.repo import SQLAlchemyRepo, TeamRepo, PointRepo, ProtocolRepo
from bot.texts.game_engine import game_text


async def start_game(repo: SQLAlchemyRepo, bot: Bot):
    teams_list = await repo.get_repo(TeamRepo).get_teams_list()
    if teams_list:
        for team in teams_list:
            await send_point(point_idx=1,
                             team_idx=team.team_id,
                             repo=repo, bot=bot)


async def send_point(point_idx: int, team_idx: int, repo: SQLAlchemyRepo, bot: Bot):
    point = await repo.get_repo(PointRepo).get_point(point_id=point_idx)
    if point.point_is_img:
        await bot.send_photo(chat_id=team_idx,
                             photo=point.point_img_id,
                             caption=f"<b>Задание №{point.point_id}</b>\n\n{point.point_text}")
        return
    await bot.send_message(chat_id=team_idx,
                           text=f"<b>Задание №{point.point_id}</b>\n\n{point.point_text}")


async def incorrect_answer(team_idx: int, point_idx: int, repo: SQLAlchemyRepo, bot: Bot):
    await bot.send_message(chat_id=team_idx, text=game_text.answer_not_correct)
    await send_point(point_idx=point_idx, team_idx=team_idx, repo=repo, bot=bot)


async def check_current_answer(answer_text: str, team_idx: int, repo: SQLAlchemyRepo, bot: Bot):
    pass

async def check_answer(answer_text: str, team_idx: int, repo: SQLAlchemyRepo, bot: Bot):
    point_idx = await repo.get_repo(ProtocolRepo).get_current_level_team(team_idx=team_idx) + 1
    correct_answer = await repo.get_repo(PointRepo).get_answer_point(point_id=point_idx)
    if answer_text.lower() == correct_answer.lower():
        await repo.get_repo(ProtocolRepo).add_endpoint(point_idx=point_idx, team_idx=team_idx)
        if not await game_is_complete(point_idx=point_idx, repo=repo):
            await send_next_point(team_idx=team_idx, point_idx=point_idx, repo=repo, bot=bot)
            return
        await end_game(team_idx=team_idx, bot=bot)
        return
    await incorrect_answer(team_idx=team_idx, point_idx=point_idx, repo=repo, bot=bot)


async def game_is_complete(point_idx: int, repo: SQLAlchemyRepo) -> bool:
    count_point = await repo.get_repo(PointRepo).get_count_point()
    if point_idx == count_point:
        return True
    return False


async def send_next_point(team_idx: int, point_idx: int, repo: SQLAlchemyRepo, bot: Bot):
    await bot.send_message(chat_id=team_idx, text=game_text.answer_correct)
    await send_point(point_idx=point_idx + 1, team_idx=team_idx, repo=repo, bot=bot)


async def end_game(team_idx: int, bot: Bot):
    await bot.send_message(chat_id=team_idx, text=await game_text.game_is_complete())
    """В теории, можно сразу вывести бота из всех групповых чатов"""


