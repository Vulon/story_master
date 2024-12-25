from pydantic import BaseModel
from datetime import datetime


class GameState(BaseModel):
    player_characters: list[str]
    current_time: datetime
    current_location: str
    current_scene: int
