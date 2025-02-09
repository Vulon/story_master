import json
import math
from datetime import timedelta

import numpy as np
from langchain_community.utils.math import cosine_similarity
from langchain_core.embeddings import Embeddings

from story_master.entities.character import ANY_CHARACTER
from story_master.entities.races import RaceType
from story_master.settings import Settings
from story_master.storage.map.map_model import (
    DetailedArea,
    Map,
    BaseLocation,
)
from story_master.storage.memory.memory_model import Observation
from story_master.storage.storage_models import CharacterStorage, GameStorage, Sim


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
            self.map = Map(locations=dict())

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

    def add_character(
        self, character: ANY_CHARACTER, is_player: bool, current_location_id: int
    ) -> Sim:
        max_id = 1
        if self.character_storage.player_characters:
            max_id = max(self.character_storage.player_characters.keys())
        if self.character_storage.npc_characters:
            max_id = max(max_id, max(self.character_storage.npc_characters.keys()))
        max_id += 1
        sim = Sim(
            id=max_id, character=character, current_location_id=current_location_id
        )
        if is_player:
            self.character_storage.player_characters[max_id] = sim
        else:
            self.character_storage.npc_characters[max_id] = sim
        self.save_characters()
        return sim

    def get_location_characters(self, location: BaseLocation) -> list[Sim]:
        sims = []
        for id, sim in self.character_storage.player_characters.items():
            if sim.current_location_id == location.id:
                sims.append(sim)
        for id, sim in self.character_storage.npc_characters.items():
            if sim.current_location_id == location.id:
                sims.append(sim)
        return sims

    def get_character_descriptions(
        self, location_id: int, character_id: int
    ) -> list[tuple[Sim, str]]:
        main_sim = self.get_sim(character_id)
        location = self.get_location(location_id)
        sims = self.get_location_characters(location)
        sims = [sim for sim in sims if sim.id != character_id]
        known_sims = [sim for sim in sims if sim.id in main_sim.character_relations]
        unknown_sims = [
            sim for sim in sims if sim.id not in main_sim.character_relations
        ]
        character_descriptions = [
            sim.character.get_stranger_description() for sim in unknown_sims
        ]
        for sim in known_sims:
            character_descriptions.append(
                f"<KnownCharacter>{sim.character.get_stranger_description()} Relations: {main_sim.character_relations[sim.id]}</KnownCharacter>"
            )
        return list(zip(unknown_sims + known_sims, character_descriptions))

    def save_map(self):
        json_text = self.map.model_dump_json(indent=2)
        self.settings.map_storage_path.write_text(json_text, encoding="utf-8")

    def save_characters(self):
        json_text = self.character_storage.model_dump_json(indent=2)
        self.settings.characters_storage_path.write_text(json_text, encoding="utf-8")

    def get_sim(self, character_id: int) -> Sim | None:
        if character_id in self.character_storage.player_characters:
            return self.character_storage.player_characters[character_id]
        if character_id in self.character_storage.npc_characters:
            return self.character_storage.npc_characters[character_id]
        return None

    def add_observation(
        self, title: str, content: str, importance: int, sim: Sim
    ) -> None:
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

    def get_memories(self, query: str, sim: Sim) -> list[Observation]:
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

    def get_existing_names(self, race: RaceType) -> set[str]:
        return {
            sim.character.name
            for sim in self.character_storage.npc_characters.values()
            if sim.character.race.name == race
        } | {
            sim.character.name
            for sim in self.character_storage.player_characters.values()
            if sim.character.race.name == race
        }

    def clear_memories(self):
        for sim in self.character_storage.player_characters.values():
            sim.memories = []
            sim.character_relations = dict()
            sim.object_memories_table = dict()
        for sim in self.character_storage.npc_characters.values():
            sim.memories = []
            sim.character_relations = dict()
            sim.object_memories_table = dict()
        self.save_characters()
