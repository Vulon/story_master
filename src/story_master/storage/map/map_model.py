from enum import StrEnum
from abc import ABC, abstractmethod
from pydantic import BaseModel


class RouteType(StrEnum):
    LAND = "land"
    ROAD = "road"
    SEA = "sea"
    RIVER = "river"


class BaseLocation(BaseModel, ABC):
    id: int
    name: str
    description: str
    parent_location: int | None

    @abstractmethod
    def get_description(self) -> str:
        pass


class LargeArea(BaseLocation):
    sub_locations: list[int] = []

    def get_description(self) -> str:
        return f"""<Location>
        id: {self.id}
        name: {self.name}
        description: {self.description}
        </Location>"""


class EnvironmentPart(BaseModel):
    id: int
    name: str
    description: str
    hidden_description: str | None
    position: tuple[int, int]
    dimensions: tuple[int, int]

    def get_description(self) -> str:
        return f"""<EnvironmentPart>
        id: {self.id}
        name: {self.name}
        description: {self.description}
        position: {self.position}
        dimensions: {self.dimensions}
        </EnvironmentPart>"""


class DetailedArea(BaseLocation):
    environment_parts: list[EnvironmentPart] = []

    def get_description(self) -> str:
        parts_description = "\n".join(
            part.get_description() for part in self.environment_parts
        )
        return f"""<Location>
        id: {self.id}
        name: {self.name}
        description: {self.description}
        environment_parts: {parts_description}
        </Location>"""


class Route(BaseModel):
    type: RouteType
    start: int
    end: int
    distance: float
    description: str


class Map(BaseModel):
    root_location: int
    locations: dict[int, LargeArea | DetailedArea]
    routes: list[Route]
