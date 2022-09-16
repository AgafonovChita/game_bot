from pydantic import BaseModel
from typing import Union


class Team(BaseModel):
    team_id: int
    team_name: Union[str, None]
    team_captain_id: Union[str, None]
