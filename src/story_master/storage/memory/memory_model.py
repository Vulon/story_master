from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel


class MemoryType(StrEnum):
    OBSERVATION = "observation"
    REFLECTION = "reflection"


class AbstractMemory(BaseModel):
    id: int
    type: MemoryType
    timestamp: datetime
    title: str
    content: str
    importance: int
    embeddings: list[float]


class Observation(AbstractMemory):
    type: Literal[MemoryType.OBSERVATION] = MemoryType.OBSERVATION


class Reflection(AbstractMemory):
    type: Literal[MemoryType.REFLECTION] = MemoryType.REFLECTION
    sources: list[int]
