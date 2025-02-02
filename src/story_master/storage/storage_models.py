from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel

from story_master.entities.character import ANY_CHARACTER
from story_master.entities.items.resources import Resource
from story_master.storage.memory.memory_model import Observation, Reflection


class Sim(BaseModel):
    id: int
    character: ANY_CHARACTER
    memories: list[Observation | Reflection] = []
    current_location_id: int
    current_status: str | None = None
    is_busy: bool = False
    character_relations: dict[int, str] = dict()
    object_memories_table: dict[int, dict[int, str]] = dict()

    def get_object_memory(self, location_id: int, object_id: int) -> str | None:
        if location_id in self.object_memories_table:
            if object_id in self.object_memories_table[location_id]:
                return self.object_memories_table[location_id][object_id]
        return None

    def set_object_memory(self, location_id: int, object_id: int, memory: str):
        if location_id not in self.object_memories_table:
            self.object_memories_table[location_id] = dict()
        self.object_memories_table[location_id][object_id] = memory

    def add_object_memory(self, location_id: int, object_id: int, memory: str):
        existing_memory = self.get_object_memory(location_id, object_id)
        if existing_memory:
            memory = f"{existing_memory}. {memory}"
        self.set_object_memory(location_id, object_id, memory)

    def delete_object_memory(self, location_id: int, object_id: int):
        if location_id in self.object_memories_table:
            if object_id in self.object_memories_table[location_id]:
                del self.object_memories_table[location_id][object_id]


class CharacterStorage(BaseModel):
    player_characters: dict[int, Sim] = dict()
    npc_characters: dict[int, Sim] = dict()


class EventType(StrEnum):
    CHARACTER_ACTION = "character_action"
    RESOURCE_GATHERED = "resource_gathered"


class GameEvent(BaseModel):
    timestamp: datetime
    type: EventType


class CharacterAction(GameEvent):
    type: Literal[EventType.CHARACTER_ACTION] = EventType.CHARACTER_ACTION
    sim_id: int
    intent: str


class ResourceGatheredEvent(GameEvent):
    type: Literal[EventType.RESOURCE_GATHERED] = EventType.RESOURCE_GATHERED
    sim_id: int
    resource: Resource
    quantity: float


class GameStorage(BaseModel):
    current_time: datetime
    events_queue: list[GameEvent] = []
