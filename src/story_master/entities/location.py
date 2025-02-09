from enum import StrEnum
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing_extensions import Literal, Self

DEFAULT_WORLD_WIDTH = 3
DEFAULT_WORLD_HEIGHT = 3


class Position(BaseModel):
    location_id: int | None
    x: int
    y: int

class BaseLocation(BaseModel, ABC):
    id: int
    name: str
    description: str
    position: Position
    sub_locations: list[int] = []

    @abstractmethod
    def get_description(self) -> str:
        pass

    def get_short_description(self) -> str:
        pass


class Object(BaseModel):
    id: int
    name: str
    description: str
    hidden_description: str | None = None
    position: Position
    width: int
    height: int

    def get_description(self, add_description: bool = True) -> str:
        lines = [
            "<Object>",
            f"id: {self.id}",
            f"name: {self.name}",
        ]
        if add_description:
            lines.append(f"description: {self.description}")
        lines += [
            f"position: {self.position.x}, {self.position.y}",
            f"size: {self.width} x {self.height}",
            "</Object>",
        ]
        return " ".join(lines)

class Building(BaseLocation):
    objects: dict[int, Object] = dict()

    def get_description(self) -> str:
        lines = [
            "<Building>",
            f"id: {self.id}",
            f"name: {self.name}",
            f"description: {self.description}",
            "</Building>",
        ]
        return " ".join(lines)

    def get_short_description(self) -> str:
        return f"(Building: {self.name})"


class Region(BaseLocation):
    objects: dict[int, Object] = dict()

    def get_description(self) -> str:
        lines = [
            "<Region>",
            f"id: {self.id}",
            f"name: {self.name}",
            f"description: {self.description}",
            "</Region>",
        ]
        return " ".join(lines)

ANY_LOCATION = Region | Building

class Map(BaseModel):
    locations: dict[int, ANY_LOCATION] = dict()
