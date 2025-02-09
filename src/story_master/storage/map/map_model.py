from enum import StrEnum
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing_extensions import Literal


# Hierarchy
# 1 - Region
# 2 - Province
# 3 - Settlement or Area (Forest, Mountain, countryside)
# 4a For settlements - District
# 4b For areas - point of interest (cave, ruins, farm)
# 5 Buildings and places

class LocationType(StrEnum):
    REGION = "Region"
    PROVINCE = "Province"
    SETTLEMENT = "Settlement"
    AREA = "Area"
    DISTRICT = "District"
    POINT_OF_INTEREST = "PointOfInterest"
    BUILDING = "Building"
    OPEN_SPACE = "OpenSpace"

class BaseLocation(BaseModel, ABC):
    type: LocationType
    id: int
    name: str
    description: str
    parent_location: int | None

    @abstractmethod
    def get_description(self) -> str:
        pass

    def get_short_description(self) -> str:
        pass

class LargeLocation(BaseLocation):
    sub_locations: list[int] = []


class Region(LargeLocation):
    type: Literal[LocationType.REGION] = LocationType.REGION

    def get_description(self) -> str:
        lines = [
            "<Region>",
            f"id: {self.id}",
            f"name: {self.name}",
            f"description: {self.description}",
            "</Region>",
        ]
        return " ".join(lines)
    def get_short_description(self) -> str:
        return f"(Large region: {self.name})"

class Province(LargeLocation):
    type: Literal[LocationType.PROVINCE] = LocationType.PROVINCE

    def get_description(self) -> str:
        lines = [
            "<Province>",
            f"id: {self.id}",
            f"name: {self.name}",
            f"description: {self.description}",
            "</Province>",
        ]
        return " ".join(lines)

    def get_short_description(self) -> str:
        return f"(Province: {self.name})"

class Settlement(LargeLocation):
    type: Literal[LocationType.SETTLEMENT] = LocationType.SETTLEMENT

    def get_description(self) -> str:
        lines = [
            "<Settlement>",
            f"id: {self.id}",
            f"name: {self.name}",
            f"description: {self.description}",
            "</Settlement>",
        ]
        return " ".join(lines)

    def get_short_description(self) -> str:
        return f"(Settlement: {self.name})"

class Area(LargeLocation):
    type: Literal[LocationType.AREA] = LocationType.AREA

    def get_description(self) -> str:
        lines = [
            "<Area>",
            f"id: {self.id}",
            f"name: {self.name}",
            f"description: {self.description}",
            "</Area>",
        ]
        return " ".join(lines)

    def get_short_description(self) -> str:
        return f"(Area: {self.name})"

class District(LargeLocation):
    type: Literal[LocationType.DISTRICT] = LocationType.DISTRICT

    def get_description(self) -> str:
        lines = [
            "<District>",
            f"id: {self.id}",
            f"name: {self.name}",
            f"description: {self.description}",
            "</District>",
        ]
        return " ".join(lines)

    def get_short_description(self) -> str:
        return f"(District: {self.name})"

class PointOfInterest(LargeLocation):
    type: Literal[LocationType.POINT_OF_INTEREST] = LocationType.POINT_OF_INTEREST

    def get_description(self) -> str:
        lines = [
            "<PointOfInterest>",
            f"id: {self.id}",
            f"name: {self.name}",
            f"description: {self.description}",
            "</PointOfInterest>",
        ]
        return " ".join(lines)

    def get_short_description(self) -> str:
        return f"(Point of interest: {self.name})"

class EnvironmentPart(BaseModel):
    id: int
    name: str
    description: str
    hidden_description: str | None = None
    position: tuple[int, int]
    dimensions: tuple[int, int]

    def get_description(self) -> str:
        lines = [
            "<EnvironmentPart>",
            f"id: {self.id}",
            f"name: {self.name}",
            f"description: {self.description}",
            f"position: {self.position}",
            f"dimensions: {self.dimensions}",
            "</EnvironmentPart>",
        ]
        return " ".join(lines)


class DetailedArea(BaseLocation):
    environment_parts: list[EnvironmentPart] = []

class BuildingType(StrEnum):
    MARKET = "Market"
    INN = "Inn"
    HOUSE = "House"
    TOWN_HALL = "Town Hall"

    BLACKSMITH = "Blacksmith"
    BAKERY = "Bakery"
    GUARDHOUSE = "Guardhouse"
    SCHOOL = "School"
    TEMPLE = "Temple"
    FARM = "Farm"
    LIBRARY = "Library"
    TAVERN = "Tavern"
    ALCHEMIST = "Alchemist"
    TAILOR = "Tailor"
    STABLE = "Stable"
    WAREHOUSE = "Warehouse"
    BATHHOUSE = "Bathhouse"
    THEATER = "Theater"
    WORKSHOP = "Workshop"
    HERBALIST = "Herbalist"

MUST_HAVE_BUILDINGS = {
    BuildingType.MARKET,
    BuildingType.INN,
    BuildingType.HOUSE,
    BuildingType.TOWN_HALL,
}



class Building(DetailedArea):
    type: Literal[LocationType.BUILDING] = LocationType.BUILDING

    def get_description(self) -> str:
        parts_description = ";".join(
            part.get_description() for part in self.environment_parts
        )
        lines = [
            "<Building>",
            f"id: {self.id}",
            f"name: {self.name}",
            f"description: {self.description}",
            f"environment_parts: {parts_description}",
            "</Building>",
        ]
        return " ".join(lines)

class OpenSpace(DetailedArea):
    type: Literal[LocationType.OPEN_SPACE] = LocationType.OPEN_SPACE

    def get_description(self) -> str:
        lines = [
            "<Place>",
            f"id: {self.id}",
            f"name: {self.name}",
            f"description: {self.description}",
            "</Place>",
        ]
        return " ".join(lines)

ANY_LOCATION = Region | Province | Settlement | Area | District | PointOfInterest | Building | OpenSpace

class Map(BaseModel):
    locations: dict[int, ANY_LOCATION]

    def get_new_id(self) -> int:
        return max(self.locations.keys()) + 1 if self.locations else 1

    def add_region(self, name: str, description: str) -> None:
        new_id = self.get_new_id()
        region = Region(id=new_id, name=name, description=description, parent_location=None)
        self.locations[new_id] = region

    def add_province(self, name: str, description: str, region: Region) -> None:
        new_id = self.get_new_id()
        province = Province(id=new_id, name=name, description=description, parent_location=region.id)
        self.locations[new_id] = province

    def add_settlement(self, name: str, description: str, province: Province) -> None:
        new_id = self.get_new_id()
        settlement = Settlement(id=new_id, name=name, description=description, parent_location=province.id)
        self.locations[new_id] = settlement

    def add_area(self, name: str, description: str, province: Province) -> None:
        new_id = self.get_new_id()
        area = Area(id=new_id, name=name, description=description, parent_location=province.id)
        self.locations[new_id] = area