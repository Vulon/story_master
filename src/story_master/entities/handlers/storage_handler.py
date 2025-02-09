from story_master.settings import Settings
from langchain_community.utils.math import cosine_similarity
from langchain_core.embeddings import Embeddings
from pydantic import BaseModel
import json
from story_master.entities.sim import Sim
from story_master.entities.location import Map, BaseLocation
from datetime import datetime

class CharacterStorage(BaseModel):
    player_characters: dict[int, Sim] = {}
    npc_characters: dict[int, Sim] = {}

class GameStorage(BaseModel):
    current_time: datetime

class StorageHandler:
    def __init__(self, settings: Settings):
        self.settings = settings

        settings.characters_storage_path.parent.mkdir(parents=True, exist_ok=True)

        if settings.characters_storage_path.exists():
            self.character_storage = CharacterStorage(
                **json.loads(
                    self.settings.characters_storage_path.read_text(encoding="utf-8")
                )
            )
        else:
            self.character_storage = CharacterStorage()

        if settings.map_storage_path.exists():
            self.map = Map(**json.loads(self.settings.map_storage_path.read_text()))
        else:
            self.map = Map()

        if settings.game_storage_path.exists():
            self.game_storage = GameStorage(
                **json.loads(
                    self.settings.game_storage_path.read_text(encoding="utf-8")
                )
            )
        else:
            self.game_storage = GameStorage(
                current_time=self.settings.default_starting_time
            )

    def get_location(self, location_id: int) -> BaseLocation:
        return self.map.locations[location_id]

    def get_sim(self, character_id: int) -> Sim | None:
        if character_id in self.character_storage.player_characters:
            return self.character_storage.player_characters[character_id]
        if character_id in self.character_storage.npc_characters:
            return self.character_storage.npc_characters[character_id]
        return None

    def save_map(self):
        json_text = self.map.model_dump_json(indent=2)
        self.settings.map_storage_path.write_text(json_text, encoding="utf-8")

    def save_characters(self):
        json_text = self.character_storage.model_dump_json(indent=2)
        self.settings.characters_storage_path.write_text(json_text, encoding="utf-8")

    def get_existing_names(self) -> set[str]:
        return {
            sim.character.name
            for sim in self.character_storage.npc_characters.values()
        } | {
            sim.character.name
            for sim in self.character_storage.player_characters.values()
        }

