from sqlalchemy import select

from bot.db.models import Script
from bot.services.repo import BaseSQLAlchemyRepo


class ScriptRepo(BaseSQLAlchemyRepo):
    async def add_script(self, script_id: int, script_name: str):
        await self._session.merge(Script(script_id=script_id,
                                         script_name=script_name))
        await self._session.commit()

    async def get_script(self):
        result = await self._session.execute(select(Script))
        return result.scalar()

    async def get_script_id(self):
        idx = await self._session.execute(select(Script.script_id))
        return idx.scalar()

    async def delete_script(self):
        await self._session.execute('DELETE FROM endpoints')
        await self._session.execute('DELETE FROM script')
        await self._session.commit()
