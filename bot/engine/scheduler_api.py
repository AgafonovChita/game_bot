from bot.services.repo import SQLAlchemyRepo, PointRepo, StateRepo
from bot.db.models import Team
from aiogram import Bot
import pendulum
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.job import Job
from apscheduler.jobstores.base import JobLookupError
from bot.texts.game_engine import tx_game_engine


async def scheduler_add_job(point_idx: int, repo: SQLAlchemyRepo, team_idx: int,
                            bot: Bot, scheduler: AsyncIOScheduler):
    point_help_timeout = await repo.get_repo(PointRepo).get_help_timeout(point_idx=point_idx)
    #  date_start = pendulum.now().add(seconds=point_help_timeout)
    date_start = pendulum.now().add(seconds=30)
    scheduler.add_job(send_help_text, 'date',
                      run_date=date_start,
                      kwargs={"point_idx": 1, "team_idx": team_idx,
                              "repo": repo, "bot": bot},
                      id=str(team_idx))


async def scheduler_remove_job(team_idx: int, scheduler: AsyncIOScheduler):
    try:
        scheduler.remove_job(job_id=str(team_idx))
    except JobLookupError:
        pass


async def send_help_text(point_idx: int, team_idx: int, repo: SQLAlchemyRepo, bot: Bot):
    point = await repo.get_repo(PointRepo).get_point(point_id=point_idx)
    if point.point_help_text_is_img:
        await bot.send_photo(chat_id=team_idx,
                             photo=point.point_help_text_img_id,
                             caption=await tx_game_engine.point_help_text(point=point))
        return
    await bot.send_message(chat_id=team_idx,
                           text=await tx_game_engine.point_help_text(point=point))
