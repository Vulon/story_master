from story_master.entities.items.items import Item
from enum import StrEnum


class ResourceType(StrEnum):
    WOOD = "Wood"
    STONE = "Stone"
    HERB = "Herb"
    IRON_ORE = "Iron Ore"
    GOLD_ORE = "Gold Ore"
    COPPER_ORE = "Copper Ore"
    WATER = "Water"
    CLAY = "Clay"
    SAND = "Sand"
    COAL = "Coal"
    SILVER_ORE = "Silver Ore"
    SALT = "Salt"
    FLINT = "Flint"
    GEMSTONE = "Gemstone"


class Resource(Item):
    name: ResourceType
    gatherable: bool = True



RESOURCES = {
    ResourceType.WOOD: Resource(
        name=ResourceType.WOOD,
        price=0.02,
        weight=2,
    ),
    ResourceType.STONE: Resource(
        name=ResourceType.STONE,
        price=0.03,
        weight=5,
    ),
    ResourceType.HERB: Resource(
        name=ResourceType.HERB,
        price=0.05,
        weight=0.1,
    ),
    ResourceType.IRON_ORE: Resource(
        name=ResourceType.IRON_ORE,
        price=2,
        weight=10,
    ),
    ResourceType.GOLD_ORE: Resource(
        name=ResourceType.GOLD_ORE,
        price=10,
        weight=10,
    ),
    ResourceType.COPPER_ORE: Resource(
        name=ResourceType.COPPER_ORE,
        price=3,
        weight=10,
    ),
    ResourceType.WATER: Resource(
        name=ResourceType.WATER,
        price=0.01,
        weight=1,
    ),
    ResourceType.CLAY: Resource(
        name=ResourceType.CLAY,
        price=0.08,
        weight=3,
    ),
    ResourceType.SAND: Resource(
        name=ResourceType.SAND,
        price=0.04,
        weight=4,
    ),
    ResourceType.COAL: Resource(
        name=ResourceType.COAL,
        price=2,
        weight=5,
    ),
    ResourceType.SILVER_ORE: Resource(
        name=ResourceType.SILVER_ORE,
        price=10,
        weight=10,
    ),
    ResourceType.SALT: Resource(
        name=ResourceType.SALT,
        price=0.5,
        weight=1,
    ),
    ResourceType.FLINT: Resource(
        name=ResourceType.FLINT,
        price=0.1,
        weight=2,
    ),
    ResourceType.GEMSTONE: Resource(
        name=ResourceType.GEMSTONE,
        price=50,
        weight=0.5,
    ),
}