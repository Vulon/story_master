from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel

from story_master.entities.location import Position


class PersonalMemoryType(StrEnum):
    OBSERVATION = "observation"
    REFLECTION = "reflection"


class AbstractPersonalMemory(BaseModel):
    id: int
    type: PersonalMemoryType
    timestamp: datetime
    title: str
    content: str
    importance: int
    embeddings: list[float]


class Observation(AbstractPersonalMemory):
    type: Literal[PersonalMemoryType.OBSERVATION] = PersonalMemoryType.OBSERVATION


class Reflection(AbstractPersonalMemory):
    type: Literal[PersonalMemoryType.REFLECTION] = PersonalMemoryType.REFLECTION
    sources: list[int]


class ObjectMemory(BaseModel):
    position: Position
    memory: str


class Relationship(BaseModel):
    character_id: int
    name: str
    text: str


class LocationMemory(BaseModel):
    location_id: int
    text: str


class Memory(BaseModel):
    plan: str = ""
    personal_memories: list[Observation | Reflection] = []
    object_memories: list[ObjectMemory] = []
    relationships: dict[int, Relationship] = dict()
    location_memories: list[LocationMemory] = []
