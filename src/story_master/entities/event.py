from typing import Literal

from pydantic import BaseModel
import datetime
from story_master.entities.location import Position
from enum import StrEnum


class ReferenceType(StrEnum):
    SIM = "sim"
    OBJECT = "object"


class EventType(StrEnum):
    SPEECH = "speech"
    SIM_SPAWN = "sim_spawn"
    OBSERVATION = "observation"


class Reference(BaseModel):
    type: ReferenceType


class SimReference(Reference):
    type: Literal[ReferenceType.SIM] = ReferenceType.SIM
    sim_id: int


class ObjectReference(Reference):
    type: Literal[ReferenceType.OBJECT] = ReferenceType.OBJECT
    position: Position


class Event(BaseModel):
    type: EventType
    description: str
    position: Position
    radius: int
    source: SimReference | ObjectReference | None = None
    target: SimReference | ObjectReference | None = None
    timestamp: datetime.datetime
