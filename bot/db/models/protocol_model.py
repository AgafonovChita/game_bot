import datetime

from sqlalchemy import Column, Integer, BigInteger, DateTime

from bot.db.base import Base


class Protocol(Base):
    __tablename__ = "protocol"
    endpoint_id = Column(Integer, primary_key=True)
    team_id = Column(BigInteger)
    point_id = Column(Integer)
    point_close_time = Column(DateTime)

    def __init__(self, team_idx: int, point_idx: int):
        self.team_id = team_idx
        self.point_id = point_idx
        self.point_close_time = datetime.datetime.now()
