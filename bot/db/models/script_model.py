from sqlalchemy import Column, BigInteger, Text, Integer

from bot.db.base import Base


class Script(Base):
    __tablename__ = "script"
    script_id = Column(BigInteger, primary_key=True, unique=True)
    script_name = Column(Text, default="NotGameName")
    script_state = Column(Integer, default=False)

    def __init__(self, script_id: int, script_name: str, script_state: int = 0):
        self.script_id = script_id
        self.script_name = script_name
        self.script_state = script_state
