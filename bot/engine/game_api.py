from bot.engine.description_api import send_description_final
from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from bot.services.repo import SQLAlchemyRepo, TeamRepo, PointRepo, ProtocolRepo, StateRepo
from bot.texts.game_engine import tx_game_engine
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from . import scheduler_api
from . import description_api


async def start_game(repo: SQLAlchemyRepo, bot: Bot, scheduler: AsyncIOScheduler):
    """Эта функция отправляет командам первое задание"""
    teams_list = await repo.get_repo(TeamRepo).get_teams_list()
    if teams_list:
        for team in teams_list:
            await send_point(point_idx=1,
                             team_idx=team.team_id,
                             repo=repo, bot=bot,
                             scheduler=scheduler)


async def stop_game(repo: SQLAlchemyRepo, bot: Bot, scheduler: AsyncIOScheduler):
    scheduler.shutdown()
    teams_list = await repo.get_repo(TeamRepo).get_teams_list()
    if teams_list:
        for team in teams_list:
            await description_api.send_description_stop_game(team_id=team.team_id,
                                                             bot=bot)
            await description_api.send_description_final(team_id=team.team_id,
                                                         bot=bot, repo=repo)




async def send_point(point_idx: int, team_idx: int,
                     repo: SQLAlchemyRepo, bot: Bot, scheduler: AsyncIOScheduler):
    point = await repo.get_repo(PointRepo).get_point(point_id=point_idx)
    await repo.get_repo(StateRepo).update_current_state(team_idx=team_idx,
                                                        point_idx=point_idx,
                                                        correct_answer=point.point_answers)
    if point.point_is_img:
        await bot.send_photo(chat_id=team_idx,
                             photo=point.point_img_id,
                             caption=await tx_game_engine.point_description(point=point))
    else:
        await bot.send_message(chat_id=team_idx,
                               text=await tx_game_engine.point_description(point=point))

    await scheduler_api.scheduler_add_job(point_idx=point_idx,
                                          team_idx=team_idx,
                                          bot=bot, repo=repo,
                                          scheduler=scheduler)


async def incorrect_answer(team_idx: int, point_idx: int, repo: SQLAlchemyRepo, bot: Bot):
    await bot.send_message(chat_id=team_idx, text=tx_game_engine.answer_not_correct)


async def check_current_answer(answer_text: str, team_idx: int,
                               repo: SQLAlchemyRepo, bot: Bot, message: types.Message,
                               scheduler: AsyncIOScheduler):
    correct_answer = await repo.get_repo(StateRepo).get_correct_answer(team_idx=team_idx)
    current_answer = await repo.get_repo(StateRepo).get_current_answer(team_idx=team_idx)
    formatted_answer = answer_text.strip()
    if formatted_answer in correct_answer.split():
        await scheduler_api.scheduler_remove_job(team_idx=team_idx, scheduler=scheduler)
        if formatted_answer not in current_answer.split():
            current_answer += f" {formatted_answer}"
            await repo.get_repo(StateRepo).update_current_answer(team_idx=team_idx,
                                                                 current_answer=current_answer)
            await message.reply(text=await tx_game_engine.get_answer_text(team_idx=team_idx,
                                                                          repo=repo,
                                                                          answer_status="ok"))
            if await level_is_complete(team_idx=team_idx, repo=repo):
                await check_level(team_idx=team_idx, repo=repo, bot=bot, scheduler=scheduler)
            return
        await message.reply(text=await tx_game_engine.get_answer_text(team_idx=team_idx,
                                                                      repo=repo,
                                                                      answer_status="repeat"))
        return
    await message.reply(text=await tx_game_engine.get_answer_text(team_idx=team_idx,
                                                                  repo=repo,
                                                                  answer_status="not_ok"))


async def check_level(team_idx: int, repo: SQLAlchemyRepo, bot: Bot, scheduler: AsyncIOScheduler):
    point_idx = await repo.get_repo(ProtocolRepo).get_current_level_team(team_idx=team_idx) + 1
    await repo.get_repo(ProtocolRepo).add_endpoint(point_idx=point_idx, team_idx=team_idx)
    if not await game_is_complete(point_idx=point_idx, repo=repo):
        await send_next_point(team_idx=team_idx, point_idx=point_idx, repo=repo, bot=bot, scheduler=scheduler)
        return
    await end_game(team_idx=team_idx, bot=bot, repo=repo)
    return


async def level_is_complete(team_idx: int, repo: SQLAlchemyRepo) -> bool:
    correct_count = await repo.get_repo(StateRepo).get_correct_count(team_idx=team_idx)
    current_count = await repo.get_repo(StateRepo).get_current_count(team_idx=team_idx)
    return correct_count == current_count


async def game_is_complete(point_idx: int, repo: SQLAlchemyRepo) -> bool:
    count_point = await repo.get_repo(PointRepo).get_count_point()
    if point_idx == count_point:
        return True
    return False


async def send_next_point(team_idx: int, point_idx: int,
                          repo: SQLAlchemyRepo, bot: Bot, scheduler: AsyncIOScheduler):
    await bot.send_message(chat_id=team_idx, text=tx_game_engine.ANSWER_CORRECT)
    await send_point(point_idx=point_idx + 1, team_idx=team_idx, repo=repo, bot=bot, scheduler=scheduler)


async def end_game(team_idx: int, bot: Bot, repo: SQLAlchemyRepo):
    await bot.send_message(chat_id=team_idx, text=await tx_game_engine.game_is_complete())
    await send_description_final(team_id=team_idx, bot=bot, repo=repo)
    """В теории, можно сразу вывести бота из всех групповых чатов"""
