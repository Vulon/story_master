from story_master.memory.entity import Entity, EntityNode
from enum import StrEnum
from gqlalchemy import Field
from story_master.db_client import get_db


db = get_db()


class LocationType(StrEnum):
    SETTLEMENT = "settlement"
    DUNGEON = "dungeon"
    WILDERNESS = "wilderness"
    LANDMARK = "landmark"
    BUILDING = "building"


class Size(StrEnum):
    TINY = "tiny"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    HUGE = "huge"


class Climate(StrEnum):
    TEMPERATE = "temperate"
    TROPICAL = "tropical"
    ARCTIC = "arctic"
    DESERT = "desert"
    COASTAL = "coastal"


CLASS_DESCRIPTION = """A location in the world. Can by any location type, such as a settlement, dungeon, wilderness, landmark or building."""

CLASS_FIELDS_DESCRIPTION = """
Fields:
- name: unique location identifier
- description: general description of the location
- location_type: one of ["settlement", "dungeon", "wilderness", "landmark", "building"]
- size: one of ["tiny", "small", "medium", "large", "huge"]
- climate: one of ["temperate", "tropical", "arctic", "desert", "coastal"]
- population: approximate number of inhabitants
- danger_level: number from 1-10 indicating how dangerous the area is
- points_of_interest: list of notable features or locations within
"""


class Location(Entity):
    name: str
    description: str
    location_type: LocationType
    size: Size
    climate: Climate
    population: int
    danger_level: int
    points_of_interest: list[str]

    @classmethod
    def get_class_description(cls) -> str:
        return CLASS_DESCRIPTION

    @classmethod
    def get_fields_description(cls):
        return CLASS_FIELDS_DESCRIPTION

    def to_dict(self) -> dict:
        model_dict = self.model_dump()
        model_dict["location_type"] = str(self.location_type)
        model_dict["size"] = str(self.size)
        model_dict["climate"] = str(self.climate)
        return model_dict


class LocationNode(EntityNode, db=db):
    name: str = Field(unique=True)
    description: str | None = None
    location_type: str
    size: str
    climate: str
    population: int
    danger_level: int
    points_of_interest: list[str]

    def to_dict(self) -> dict:
        model_dict = self.model_dump()
        model_dict["location_type"] = LocationType[self.location_type]
        model_dict["size"] = Size[self.size]
        model_dict["climate"] = Climate[self.climate]
        return model_dict
