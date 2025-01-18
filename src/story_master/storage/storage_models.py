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
    current_location_id: int | None = None
    current_status: str | None = None
    is_busy: bool = False

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

