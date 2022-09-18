from sqlalchemy import Column, Integer, Text, Boolean

from bot.db.base import Base


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
