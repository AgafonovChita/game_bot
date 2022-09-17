from sqlalchemy import select

from bot.db.models import Script, CurrentState
from bot.services.repo import BaseSQLAlchemyRepo


class StateRepo(BaseSQLAlchemyRepo):
    async def add_current_state(self, team_idx: int, point_idx: int, correct_answer: str):


        await self._session.merge(CurrentState(team_id=team_idx,
                                               point_id=point_idx,
                                               correct_answer=correct_answer))
        await self._session.commit()

