from enum import StrEnum
from story_master.entities.items.items import Item


class ArmorCategory(StrEnum):
    LIGHT_ARMOR = "Light Armor"
    MEDIUM_ARMOR = "Medium Armor"
    HEAVY_ARMOR = "Heavy Armor"
    SHIELD = "Shield"


class Armor(Item):
    armor_class: int
    armor_category: ArmorCategory
    uses_agility: bool
    max_agility_bonus: int
    strength_requirement: int
    strealth_disadvantage: bool


class ArmorType(StrEnum):
    PADDED = "Padded"
    LEATHER = "Leather"
    STUDDED_LEATHER = "Studded Leather"
    HIDE = "Hide"
    CHAIN_SHIRT = "Chain Shirt"
    SCALE_MAIL = "Scale Mail"
    BREASTPLATE = "Breastplate"
    HALF_PLATE = "Half Plate"
    RING_MAIL = "Ring Mail"
    CHAIN_MAIL = "Chain Mail"
    SPLINT = "Splint"
    PLATE = "Plate"
    SHIELD = "Shield"


ARMORS = {
    ArmorType.PADDED: Armor(
        name=ArmorType.PADDED,
        price=5,
        weight=8,
        armor_class=11,
        armor_category=ArmorCategory.LIGHT_ARMOR,
        uses_agility=True,
        max_agility_bonus=None,
        strength_requirement=0,
        strealth_disadvantage=True,
    ),
    ArmorType.LEATHER: Armor(
        name=ArmorType.LEATHER,
        price=10,
        weight=10,
        armor_class=11,
        armor_category=ArmorCategory.LIGHT_ARMOR,
        uses_agility=True,
        max_agility_bonus=None,
        strength_requirement=0,
        strealth_disadvantage=False,
    ),
    ArmorType.STUDDED_LEATHER: Armor(
        name=ArmorType.STUDDED_LEATHER,
        price=45,
        weight=13,
        armor_class=12,
        armor_category=ArmorCategory.LIGHT_ARMOR,
        uses_agility=True,
        max_agility_bonus=None,
        strength_requirement=0,
        strealth_disadvantage=False,
    ),
    ArmorType.HIDE: Armor(
        name=ArmorType.HIDE,
        price=10,
        weight=12,
        armor_class=12,
        armor_category=ArmorCategory.MEDIUM_ARMOR,
        uses_agility=True,
        max_agility_bonus=2,
        strength_requirement=0,
        strealth_disadvantage=False,
    ),
    ArmorType.CHAIN_SHIRT: Armor(
        name=ArmorType.CHAIN_SHIRT,
        price=50,
        weight=20,
        armor_class=13,
        armor_category=ArmorCategory.MEDIUM_ARMOR,
        uses_agility=True,
        max_agility_bonus=2,
        strength_requirement=0,
        strealth_disadvantage=False,
    ),
    ArmorType.SCALE_MAIL: Armor(
        name=ArmorType.SCALE_MAIL,
        price=50,
        weight=45,
        armor_class=14,
        armor_category=ArmorCategory.MEDIUM_ARMOR,
        uses_agility=True,
        max_agility_bonus=2,
        strength_requirement=0,
        strealth_disadvantage=True,
    ),
    ArmorType.BREASTPLATE: Armor(
        name=ArmorType.BREASTPLATE,
        price=400,
        weight=20,
        armor_class=14,
        armor_category=ArmorCategory.MEDIUM_ARMOR,
        uses_agility=True,
        max_agility_bonus=2,
        strength_requirement=0,
        strealth_disadvantage=False,
    ),
    ArmorType.HALF_PLATE: Armor(
        name=ArmorType.HALF_PLATE,
        price=750,
        weight=40,
        armor_class=15,
        armor_category=ArmorCategory.MEDIUM_ARMOR,
        uses_agility=True,
        max_agility_bonus=2,
        strength_requirement=0,
        strealth_disadvantage=True,
    ),
    ArmorType.RING_MAIL: Armor(
        name=ArmorType.RING_MAIL,
        price=30,
        weight=40,
        armor_class=14,
        armor_category=ArmorCategory.HEAVY_ARMOR,
        uses_agility=False,
        max_agility_bonus=None,
        strength_requirement=0,
        strealth_disadvantage=True,
    ),
    ArmorType.CHAIN_MAIL: Armor(
        name=ArmorType.CHAIN_MAIL,
        price=75,
        weight=55,
        armor_class=16,
        armor_category=ArmorCategory.HEAVY_ARMOR,
        uses_agility=False,
        max_agility_bonus=None,
        strength_requirement=13,
        strealth_disadvantage=True,
    ),
    ArmorType.SPLINT: Armor(
        name=ArmorType.SPLINT,
        price=200,
        weight=60,
        armor_class=17,
        armor_category=ArmorCategory.HEAVY_ARMOR,
        uses_agility=False,
        max_agility_bonus=None,
        strength_requirement=15,
        strealth_disadvantage=True,
    ),
    ArmorType.PLATE: Armor(
        name=ArmorType.PLATE,
        price=1500,
        weight=65,
        armor_class=18,
        armor_category=ArmorCategory.HEAVY_ARMOR,
        uses_agility=False,
        max_agility_bonus=None,
        strength_requirement=15,
        strealth_disadvantage=True,
    ),
    ArmorType.SHIELD: Armor(
        name=ArmorType.SHIELD,
        price=10,
        weight=6,
        armor_class=2,
        armor_category=ArmorCategory.SHIELD,
        uses_agility=False,
        max_agility_bonus=None,
        strength_requirement=0,
        strealth_disadvantage=False,
    ),
}
