import datetime

from sqlalchemy import select, update

from bot.db.models import Game
from bot.services.repo import BaseSQLAlchemyRepo


class GameRepo(BaseSQLAlchemyRepo):
    async def get_game_state(self):
        game = await self._session.execute(select(Game.game_state))
        await self._session.commit()
        return game.scalar()

    async def schedule_game(self, game_id: int):
        await self._session.merge(Game(game_id=game_id,
                                       game_state=1))
        await self._session.commit()

    async def cancel_game(self):
        pass

    async def start_game(self, game_id: int = 1):
        await self._session.execute(update(Game).
                                    where(Game.game_id == game_id).
                                    values(game_state=2, game_start=datetime.datetime.now()))
        await self._session.commit()

    async def stop_game(self, game_id: int):
        await self._session.execute(update(Game).
                                    where(Game.game_id == game_id).
                                    values(game_state=3, game_end=datetime.datetime.now()))
        await self._session.commit()

    async def reset_game(self):
        await self._session.execute('DELETE FROM game')
        await self._session.commit()

    async def get_description_start(self):
        description_start = await self._session.execute(select(Game.description_start))
        await self._session.commit()
        return description_start.scalar()

    async def get_description_final(self):
        description_final = await self._session.execute(select(Game.description_final))
        await self._session.commit()
        return description_final.scalar()

    async def update_description_start(self, game_id: int, description_text: str):
        await self._session.execute(update(Game).
                                    where(Game.game_id == game_id).
                                    values(description_start=description_text))
        await self._session.commit()

    async def update_description_final(self, game_id: int, description_text: str):
        await self._session.execute(update(Game).
                                    where(Game.game_id == game_id).
                                    values(description_final=description_text))
        await self._session.commit()




