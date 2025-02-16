from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel


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
    location_id: int
    x: int
    y: int
    memory: str


class Relationship(BaseModel):
    name: str
    character_id: int
    text: str


class LocationMemory(BaseModel):
    location_id: int
    text: str


class Memory(BaseModel):
    plan: str = ""
    personal_memories: list[Observation | Reflection] = []
    object_memories: list[ObjectMemory] = []
    relationships: list[Relationship] = []
    location_memories: list[LocationMemory] = []
