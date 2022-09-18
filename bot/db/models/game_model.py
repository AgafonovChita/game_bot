from sqlalchemy import Column, BigInteger, Integer, DateTime, Text

from bot.db.base import Base


class Game(Base):
    __tablename__ = "game"
    game_id = Column(BigInteger, primary_key=True)
    game_state = Column(Integer, default=0)
    game_start = Column(DateTime, default=None)
    game_end = Column(DateTime, default=None)
    description_start = Column(Text, default="\U000025B6 Стартовая инструкция")
    description_final = Column(Text, default="\U0001F3C1 Финальная инструкция")
