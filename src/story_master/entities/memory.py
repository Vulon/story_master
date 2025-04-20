from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel

from story_master.entities.location import Position


class MemoryTag(StrEnum):
    RELATIONSHIP = "relationship"
    LOCATION = "location"
    INVENTORY = "inventory"
    PLAN = "plan"
    OBJECT = "object"


class MemoryEntry(BaseModel):
    id: int
    content: str
    timestamp: datetime
    tag: MemoryTag | None = None
    importance: int
    related_entity_id: int | None = None
    position: Position | None = None


class Memory(BaseModel):
    entries: list[MemoryEntry] = []
    plan: str = ""
