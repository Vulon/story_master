import json
import math
from datetime import datetime, timedelta

import numpy as np
from langchain_community.utils.math import cosine_similarity
from langchain_core.embeddings import Embeddings
from pydantic import BaseModel

from story_master.entities.character import Character
from story_master.settings import Settings
from story_master.storage.map.base_map import DEFAULT_MAP
from story_master.storage.map.map_model import Location, Map
from story_master.storage.memory.memory_model import Observation, Reflection


class Sim(BaseModel):
    character: Character
    memories: list[Observation | Reflection] = []
    current_location_id: int | None = None
    current_status: str | None = None


class CharacterStorage(BaseModel):
    player_characters: list[Sim] = []
    npc_characters: list[Sim] = []


class GameStorage(BaseModel):
    current_time: datetime


class StorageManager:
    def __init__(self, settings: Settings, embeddings_client: Embeddings):
        self.settings = settings
        self.embeddings_client = embeddings_client
        settings.characters_storage_path.parent.mkdir(parents=True, exist_ok=True)
        settings.map_storage_path.parent.mkdir(parents=True, exist_ok=True)
        settings.game_storage_path.parent.mkdir(parents=True, exist_ok=True)
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
            self.map = DEFAULT_MAP

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

    def get_location(self, location_id: int) -> Location:
        return [
            location for location in self.map.locations if location.id == location_id
        ][0]

    def get_child_locations(self, location_id: int) -> list[Location]:
        return [
            location
            for location in self.map.locations
            if location.parent_location == location_id
        ]

    def save_map(self):
        json_text = self.map.model_dump_json(indent=2)
        self.settings.map_storage_path.write_text(json_text, encoding="utf-8")

    def save_characters(self):
        json_text = self.character_storage.model_dump_json(indent=2)
        self.settings.characters_storage_path.write_text(json_text, encoding="utf-8")

    def get_sim(self, character: Character) -> Sim | None:
        for sim in self.character_storage.player_characters:
            if sim.character is character:
                return sim
        for sim in self.character_storage.npc_characters:
            if sim.character is character:
                return sim
        return None

    def add_observation(
        self, title: str, content: str, importance: int, character: Character
    ) -> None:
        sim = self.get_sim(character)
        embeddings = self.embeddings_client.embed_query(content)
        memory_ids = [memory.id for memory in sim.memories]
        max_id = max(memory_ids) + 1 if memory_ids else 0
        timestamp = self.game_storage.current_time
        self.game_storage.current_time = self.game_storage.current_time + timedelta(
            seconds=1
        )
        memory = Observation(
            id=max_id,
            timestamp=timestamp,
            title=title,
            content=content,
            importance=importance,
            embeddings=embeddings,
        )
        sim.memories.append(memory)
        self.save_characters()

    def get_memories(self, query: str, character: Character) -> list[Observation]:
        sim = self.get_sim(character)
        query_embeddings = self.embeddings_client.embed_query(query)
        query_embeddings = np.array(query_embeddings).reshape(1, -1)
        current_time = self.game_storage.current_time
        scored_memories = []
        for memory in sim.memories:
            memory_embeddings = np.array(memory.embeddings).reshape(1, -1)
            distance = cosine_similarity(query_embeddings, memory_embeddings)
            time_difference = current_time - memory.timestamp
            importance = memory.importance
            score = (
                distance
                * importance
                / max(math.log(time_difference.total_seconds() / 60 + 1), 1)
            )
            scored_memories.append((memory, score))
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        return [
            memory
            for memory, _ in scored_memories[: self.settings.max_similar_memories]
        ]
