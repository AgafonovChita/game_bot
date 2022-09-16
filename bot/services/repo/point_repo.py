from sqlalchemy import select, func

from bot.db.models import Endpoint
from bot.services.repo import BaseSQLAlchemyRepo


class PointRepo(BaseSQLAlchemyRepo):
    async def add_point(self, point: dict):
        await self._session.merge(Endpoint(point_text=point.get("text_point"),
                                           point_is_img=point.get("point_is_img"),
                                           point_img_id=point.get("point_img_id"),
                                           point_help_text=point.get("help_text"),
                                           point_help_text_is_img=point.get("point_help_text_is_img"),
                                           point_help_text_img_id=point.get("point_help_text_img_id"),
                                           point_answers=point.get("answers"),
                                           point_help_timeout=point.get("timeout")))
        await self._session.commit()

    async def get_count_point(self):
        result = await self._session.execute(select(func.count()).select_from(select(Endpoint).subquery()))
        return result.scalar_one()

    async def get_points_list(self):
        result = await self._session.execute(select(Endpoint))
        return result.scalars().all()

    async def get_point(self, point_id: int) -> Endpoint:
        sql = select(Endpoint).where(Endpoint.point_id == point_id)
        result = await self._session.execute(sql)
        return result.scalar()

    async def get_answer_point(self, point_id: int):
        sql = select(Endpoint.point_answers).where(Endpoint.point_id == point_id)
        result = await self._session.execute(sql)
        return result.scalar()


    async def check_point(self, point_id: int):
        return bool(await self._session.get(Endpoint, point_id))

    async def delete_point(self, point_id: int):
        request = await self._session.get(Endpoint, point_id)
        result = await self._session.delete(request)
        await self._session.commit()
        return result
