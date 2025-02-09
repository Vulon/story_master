from datetime import datetime
from pathlib import Path

from pydantic_settings import BaseSettings

ROOT = Path(__file__).parents[2]


class Settings(BaseSettings):
    characters_storage_path: Path = ROOT / "data" / "characters.json"
    map_storage_path: Path = ROOT / "data" / "map.json"
    game_storage_path: Path = ROOT / "data" / "game.json"
    main_player_id: int = 0

    default_starting_time: datetime = datetime(1410, 5, 1, 10, 0, 0)

