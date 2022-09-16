import datetime

from sqlalchemy import select, func

from bot.db.models import Protocol
from bot.services.repo import BaseSQLAlchemyRepo


class ProtocolRepo(BaseSQLAlchemyRepo):
    async def reset_protocol(self):
        await self._session.execute('DELETE FROM protocol')
        await self._session.commit()

    async def get_current_level_team(self, team_idx: int):
        current_level = await self._session.execute(select(func.count()).
                                                    select_from(select(Protocol).where(Protocol.team_id == team_idx).
                                                                subquery()))
        return current_level.scalar_one()

    async def add_endpoint(self, point_idx: int, team_idx: int):
        await self._session.merge(Protocol(point_idx=point_idx, team_idx=team_idx))
        await self._session.commit()

