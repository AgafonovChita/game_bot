from sqlalchemy import select, delete
from typing import List
from bot.db.models import Team
from bot.services.repo import BaseSQLAlchemyRepo


class TeamRepo(BaseSQLAlchemyRepo):
    async def add_team(self, team_id: int, team_name: str, captain_username: str):
        await self._session.merge(Team(team_id=team_id,
                                       team_name=team_name,
                                       captain_username=captain_username))
        await self._session.commit()

    async def delete_team(self, team_idx: int):
        await self._session.execute(delete(Team).where(Team.team_id == team_idx))
        await self._session.commit()


    async def get_teams_list(self) -> List[Team]:
        teams = await self._session.execute(select(Team))
        return teams.scalars().all()

    async def reset_teams(self):
        await self._session.execute('DELETE FROM teams')
        await self._session.commit()
