from sqlalchemy import Column, BigInteger, Text

from bot.db.base import Base


class Team(Base):
    __tablename__ = "teams"
    team_id = Column(BigInteger, primary_key=True, unique=True)
    team_name = Column(Text, default="NotName")
    team_captain_username = Column(Text, default="NotNameCaptain")

    def __init__(self, team_id, team_name, captain_username):
        self.team_id = team_id
        self.team_name = team_name
        self.team_captain_username = captain_username
