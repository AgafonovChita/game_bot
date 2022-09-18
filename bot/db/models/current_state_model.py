from sqlalchemy import Column, BigInteger, Integer, Text, PickleType
from apscheduler.job import Job

from bot.db.base import Base


class CurrentState(Base):
    __tablename__ = "current_state"
    team_id = Column(BigInteger, primary_key=True)
    point_id = Column(Integer)
    current_answer = Column(Text, default="")
    current_count = Column(Integer, default=0)
    correct_answer = Column(Text)
    correct_count = Column(Integer)
    job = Column(PickleType, default=None)

    def __init__(self, team_idx: int, point_idx: int, correct_answer: str,
                 correct_count: int, current_count: int = 0, current_answer: int = ""):
        self.team_id = team_idx
        self.point_id = point_idx
        self.current_answer = current_answer
        self.correct_answer = correct_answer
        self.current_count = current_count
        self.correct_count = correct_count
