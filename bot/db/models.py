import datetime

from sqlalchemy import Column, BigInteger, Text, DateTime, Boolean, Integer
from sqlalchemy.dialects.sqlite import DATETIME

from bot.db.base import Base
from sqlalchemy.sql import func


class Team(Base):
    __tablename__ = "teams"
    team_id = Column(BigInteger, primary_key=True, unique=True)
    team_name = Column(Text, default="NotName")
    team_captain_username = Column(Text, default="NotNameCaptain")

    def __init__(self, team_id, team_name, captain_username):
        self.team_id = team_id
        self.team_name = team_name
        self.team_captain_username = captain_username


class Game(Base):
    __tablename__ = "game"
    game_id = Column(BigInteger, primary_key=True)
    game_state = Column(Integer, default=0)
    game_start = Column(DateTime, default=None)
    game_end = Column(DateTime, default=None)


class Script(Base):
    __tablename__ = "script"
    script_id = Column(BigInteger, primary_key=True, unique=True)
    script_name = Column(Text, default="NotGameName")
    script_state = Column(Integer, default=False)

    def __init__(self, script_id: int, script_name: str, script_state: int = 0):
        self.script_id = script_id
        self.script_name = script_name
        self.script_state = script_state


class Endpoint(Base):
    __tablename__ = "endpoints"
    point_id = Column(Integer, primary_key=True)

    point_text = Column(Text, default=None)
    point_is_img = Column(Boolean, default=False)
    point_img_id = Column(Text, default=None)

    point_help_text = Column(Text, default=None)
    point_help_text_is_img = Column(Boolean, default=False)
    point_help_text_img_id = Column(Text, default=None)
    point_answers = Column(Text, default=None)
    point_help_timeout = Column(Integer, default=600)

    def __init__(self, point_text: str, point_is_img: bool, point_img_id: str,
                 point_answers: str, point_help_text: str, point_help_text_img_id: str,
                 point_help_text_is_img: bool, point_help_timeout: int):
        self.point_text = point_text
        self.point_is_img = point_is_img
        self.point_img_id = point_img_id
        self.point_help_text = point_help_text
        self.point_help_text_is_img = point_help_text_is_img
        self.point_help_text_img_id = point_help_text_img_id
        self.point_answers = point_answers
        self.point_help_timer = point_help_timeout


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


class CurrentState(Base):
    __tablename__ = "current_state"
    team_id = Column(BigInteger, primary_key=True)
    point_id = Column(Integer)
    current_answer = Column(Text, default="")
    current_count = Column(Integer, default=0)
    correct_answer = Column(Text)
    correct_count = Column(Integer)

    def __init__(self, team_idx: int, point_idx: int, correct_answer: str,
                 correct_count: int, current_count: int = 0, current_answer: int = ""):
        self.team_id = team_idx
        self.point_id = point_idx
        self.current_answer = current_answer
        self.correct_answer = correct_answer
        self.current_count = current_count
        self.correct_count = correct_count








