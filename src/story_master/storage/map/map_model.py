from enum import StrEnum

from pydantic import BaseModel


class RouteType(StrEnum):
    LAND = "land"
    ROAD = "road"
    SEA = "sea"
    RIVER = "river"


class Location(BaseModel):
    id: int
    name: str
    description: str
    short_description: str
    parent_location: int | None
    is_leaf: bool = False
    interior: str | None = None

    def get_full_description(self) -> str:
        return f"""<Location>
        id: {self.id}
        name: {self.name}
        description: {self.description}
        interior: {self.interior}
        </Location>
        """


class Route(BaseModel):
    type: RouteType
    start: int
    end: int
    distance: float
    description: str


class Map(BaseModel):
    locations: list[Location]
    routes: list[Route]
