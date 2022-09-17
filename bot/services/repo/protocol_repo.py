import datetime

from sqlalchemy import select, func

from bot.db.models import Protocol, Team
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

    async def get_current_protocol_list(self):
        current_protocol_list = await self._session.execute(
            select([Team.team_name, func.max(Protocol.point_id).label("point_id"), Protocol.point_close_time]).
            group_by(Protocol.team_id).
            where(Team.team_id == Protocol.team_id))
        await self._session.commit()
        return current_protocol_list.all()

    async def get_current_protocol_to_export(self):
        current_protocol = await self._session.execute(
            select([Team.team_name, Protocol.point_id, Protocol.point_close_time]).
            where(Team.team_id == Protocol.team_id))
        await self._session.commit()
        return current_protocol.all()

    async def get_final_protocol_to_export(self):
        final_protocol = await self._session.execute(select([Team.team_name,
                                                             func.max(Protocol.point_id).label("point_id"),
                                                             func.max(Protocol.point_close_time).label("finish_time")]).
                                                     group_by(Team.team_id).
                                                     order_by(Protocol.point_id.desc(),
                                                              Protocol.point_close_time).
                                                     where(Team.team_id == Protocol.team_id))
        await self._session.commit()
        return final_protocol.all()
