from pydantic import BaseModel
from enum import StrEnum
from story_master.entities.allignment import Allignment
from story_master.entities.characteristics import Size
from story_master.entities.perks import Perk, PerkType, PERKS
from story_master.entities.items import (
    ArmorType,
    WeaponType,
    InstrumentType,
    ArmorCategory,
)


class RaceType(StrEnum):
    HUMAN = "Human"
    ELF = "Elf"
    HIGH_ELF = "High Elf"
    FOREST_ELF = "Forest Elf"
    DROW = "Drow"
    DWARF = "Dwarf"
    MOUNTAIN_DWARF = "Mountain Dwarf"
    HILL_DWARF = "Hill Dwarf"
    HALFLING = "Halfling"
    ORC = "Orc"


class Race(BaseModel):
    name: RaceType
    note: str = ""
    strength_bonus: int = 0
    agility_bonus: int = 0
    constitution_bonus: int = 0
    intelligence_bonus: int = 0
    wisdom_bonus: int = 0
    charisma_bonus: int = 0
    lifespan: int
    names: list[str]
    default_allignment: Allignment
    size: Size
    movement_speed: int
    perks: list[Perk] = []
    weapon_proficiencies: list[WeaponType] = []
    instrument_proficiencies: list[InstrumentType] = []
    armor_proficiencies: list[ArmorType] = []


DWARF = Race(
    name=RaceType.DWARF,
    streangth_bonus=2,
    lifespan=350,
    default_allignment=Allignment.LAWFUL_GOOD,
    constitution_bonus=2,
    size=Size.MEDIUM,
    movement_speed=25,
    perks=[
        PERKS[PerkType.NIGHT_VISION],
        PERKS[PerkType.DWARVEN_RESILIENCE],
        PERKS[PerkType.STONECUNNING],
    ],
    weapon_proficiencies=[
        WeaponType.BATTLEAXE,
        WeaponType.HANDAXE,
        WeaponType.LIGHT_HAMMER,
        WeaponType.WARHAMMER,
    ],
    instrument_proficiencies=[
        InstrumentType.SMITHS_TOOLS,
        InstrumentType.BREWERS_TOOLS,
        InstrumentType.MASONS_TOOLS,
    ],
    names=[
        "Adrik",
        "Alberich",
        "Barend",
        "Baern",
        "Brottor",
        "Bruenor",
        "Vondal",
        "Veit",
        "Gardain",
        "Dain",
        "Darrak",
        "Delg",
        "Kildrak",
        "Morgran",
        "Orsik",
        "Oskar",
        "Rangrim",
        "Rurik",
        "Taklinn",
        "Toradin",
        "Tordek",
        "Torin",
        "Travok",
        "Traubon",
        "Ulfgar",
        "Fargrim",
        "Flint",
        "Harbeck",
        "Eberk",
        "Einkil",
        "Artin",
        "Bardrin",
        "Vistra",
        "Gunnloda",
        "Gurdis",
        "Dagnal",
        "Dieza",
        "Ilde",
        "Katra",
        "Kristid",
        "Liftrasa",
        "Mardred",
        "Odhild",
        "Riswin",
        "Sannl",
        "Torbera",
        "Torgga",
        "Falkrunn",
        "Finellen",
        "Heldja",
        "Hlin",
        "Eldeth",
        "Ember",
    ],
)

ELF = Race(
    name=RaceType.ELF,
    lifespan=700,
    names=[
        "Adran",
        "Aramil",
        "Arannis",
        "Aust",
        "Aelar",
        "Beiro",
        "Berrian",
        "Varis",
        "Galindan",
        "Ivelios",
        "Immeral",
        "Carric",
        "Quarion",
        "Lausian",
        "Mindartis",
        "Paelias",
        "Peren",
        "Riardon",
        "Rolen",
        "Soveliss",
        "Tamior",
        "Tarivol",
        "Theren",
        "Hadarai",
        "Himo",
        "Heian",
        "Enialis",
        "Erdan",
        "Erevan",
    ],
    agility_bonus=2,
    default_allignment=Allignment.CHAOTIC_GOOD,
    size=Size.MEDIUM,
    movement_speed=30,
    perks=[
        PERKS[PerkType.NIGHT_VISION],
        PERKS[PerkType.FEY_ANCESTRY],
        PERKS[PerkType.PERCEPTION],
    ],
)

RACES = [
    DWARF.model_copy(
        name=RaceType.MOUNTAIN_DWARF,
        strength_bonus=2,
        armor_proficiencies=[ArmorCategory.MEDIUM_ARMOR, ArmorCategory.LIGHT_ARMOR],
    ),
    DWARF.model_copy(
        name=RaceType.HILL_DWARF,
        wisdom_bonus=1,
        perks=[
            PERKS[PerkType.DWARVEN_TOUGHNESS],
            PERKS[PerkType.NIGHT_VISION],
            PERKS[PerkType.DWARVEN_RESILIENCE],
            PERKS[PerkType.STONECUNNING],
        ],
    ),
    ELF.model_copy(
        name=RaceType.HIGH_ELF,
        intelligence_bonus=1,
        weapon_proficiencies=[
            WeaponType.LONGSWORD,
            WeaponType.SHORTSWORD,
            WeaponType.SHORTBOW,
            WeaponType.LONG_BOW,
        ],
        # TODO: Add cantrip
    ),
    ELF.model_copy(
        name=RaceType.FOREST_ELF,
        wisdom_bonus=1,
        movement_speed=35,
        weapon_proficiencies=[
            WeaponType.LONGSWORD,
            WeaponType.SHORTSWORD,
            WeaponType.SHORTBOW,
            WeaponType.LONG_BOW,
        ],
        perks=[
            PERKS[PerkType.NIGHT_VISION],
            PERKS[PerkType.FEY_ANCESTRY],
            PERKS[PerkType.PERCEPTION],
            PERKS[PerkType.WILDERNESS_CAMOUFLAGE],
        ],
    ),
    ELF.model_copy(
        name=RaceType.DROW,
        charisma_bonus=1,
        weapon_proficiencies=[
            WeaponType.RAPIER,
            WeaponType.SHORTSWORD,
            WeaponType.HAND_CROSSBOW,
        ],
        perks=[
            PERKS[PerkType.PERFECT_NIGHT_VISION],
            PERKS[PerkType.FEY_ANCESTRY],
            PERKS[PerkType.PERCEPTION],
            PERKS[PerkType.SUNLIGHT_SENSITIVITY],
            PERKS[PerkType.DROW_MAGIC],
        ],
    ),
]
