from sqlalchemy import select, update

from bot.db.models import Script, CurrentState
from bot.services.repo import BaseSQLAlchemyRepo
from apscheduler.job import Job


class StateRepo(BaseSQLAlchemyRepo):
    async def update_current_state(self, team_idx: int, point_idx: int, correct_answer: str):
        await self._session.merge(CurrentState(team_idx=team_idx,
                                               point_idx=point_idx,
                                               correct_answer=correct_answer,
                                               correct_count=len(correct_answer.split())))
        await self._session.commit()

    async def get_correct_answer(self, team_idx) -> str:
        correct_answer = await self._session.execute(select(CurrentState.correct_answer).
                                                     where(CurrentState.team_id == team_idx))
        return correct_answer.scalar_one()

    async def get_current_answer(self, team_idx) -> str:
        current_answer = await self._session.execute(select(CurrentState.current_answer).
                                                     where(CurrentState.team_id == team_idx))
        return current_answer.scalar_one()

    async def update_current_answer(self, team_idx: int, current_answer: str):
        await self._session.execute(update(CurrentState).
                                    where(CurrentState.team_id == team_idx).
                                    values(current_answer=current_answer))
        await self._session.execute(update(CurrentState).
                                    where(CurrentState.team_id == team_idx).
                                    values(current_count=CurrentState.current_count + 1))
        await self._session.commit()

    async def get_current_count(self, team_idx: int):
        current_count = await self._session.execute(select(CurrentState.current_count).
                                                    where(CurrentState.team_id == team_idx))
        return current_count.scalar_one()

    async def get_correct_count(self, team_idx: int):
        current_count = await self._session.execute(select(CurrentState.correct_count).
                                                    where(CurrentState.team_id == team_idx))
        return current_count.scalar_one()

    async def reset_state(self):
        await self._session.execute('DELETE FROM current_state')
        await self._session.commit()

    async def update_job(self, team_idx: int, job_instance: Job):
        await self._session.execute(update(CurrentState).
                                    where(CurrentState.team_id == team_idx).
                                    values(job=job_instance))
        await self._session.commit()

    async def get_job(self, team_idx: int):
        job = await self._session.execute(select(CurrentState.job).
                                          where(CurrentState.team_id == team_idx))
        await self._session.commit()
        return job

