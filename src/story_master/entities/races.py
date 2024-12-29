from pydantic import BaseModel
from enum import StrEnum
from story_master.entities.allignment import Allignment
from story_master.entities.characteristics import Size
from story_master.entities.perks import Perk, PerkType, PERKS
from story_master.entities.characteristics import SkillType, SKILL_CONDITIONS
from story_master.entities.items import (
    ArmorType,
    WeaponType,
    InstrumentType,
    ArmorCategory,
    INSTRUMENTS,
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
    description: str
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
    skills: list[SkillType] = []
    weapon_proficiencies: list[WeaponType] = []
    instrument_proficiencies: list[InstrumentType] = []
    armor_proficiencies: list[ArmorType] = []

    def get_full_description(self, include_names: bool = False) -> str:
        output = f"""<Race>
        type: {self.name}
        description: {self.description}
        lifespan: {self.lifespan}
        default_allignment: {self.default_allignment}
        {"Names: " + ", ".join(self.names) if include_names else ""}
        size: {self.size}
        movement_speed: {self.movement_speed}
        perks: [{"; ".join([perk.get_full_description() for perk in self.perks])}]
        skills: [{"; ".join([f" {skill.value}: {SKILL_CONDITIONS[skill]} " for skill in self.skills])}]
        weapon_proficiencies: [{"; ".join([weapon.value for weapon in self.weapon_proficiencies])}]
        instrument_proficiencies: [{"; ".join([INSTRUMENTS[instrument].get_full_description() for instrument in self.instrument_proficiencies])}]
        armor_proficiencies: [{"; ".join([armor.value for armor in self.armor_proficiencies])}]
        </Race>
        """
        return output


DWARF = Race(
    description="",
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
    description="",
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
    ],
    skills=[SkillType.PERCEPTION],
)

RACES = {
    RaceType.MOUNTAIN_DWARF: DWARF.model_copy(
        update=dict(
            name=RaceType.MOUNTAIN_DWARF,
            description="You are a mountain dwarf, a breed of dwarf that lives in the mountains and is known for its strength and endurance.",
            strength_bonus=2,
            armor_proficiencies=[ArmorCategory.MEDIUM_ARMOR, ArmorCategory.LIGHT_ARMOR],
        )
    ),
    RaceType.HILL_DWARF: DWARF.model_copy(
        update=dict(
            name=RaceType.HILL_DWARF,
            description="You are a hill dwarf, a breed of dwarf that lives in the hills and is known for its wisdom and resilience.",
            wisdom_bonus=1,
            perks=[
                PERKS[PerkType.DWARVEN_TOUGHNESS],
                PERKS[PerkType.NIGHT_VISION],
                PERKS[PerkType.DWARVEN_RESILIENCE],
                PERKS[PerkType.STONECUNNING],
            ],
        )
    ),
    RaceType.HIGH_ELF: ELF.model_copy(
        update=dict(
            name=RaceType.HIGH_ELF,
            description="You are a high elf, you are tall, fair, and have a natural talent for magic.",
            intelligence_bonus=1,
            weapon_proficiencies=[
                WeaponType.LONGSWORD,
                WeaponType.SHORTSWORD,
                WeaponType.SHORTBOW,
                WeaponType.LONG_BOW,
            ],
            # TODO: Add cantrip
        )
    ),
    RaceType.FOREST_ELF: ELF.model_copy(
        update=dict(
            name=RaceType.FOREST_ELF,
            description="You are a forest elf, you are a skilled archer and tracker.",
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
                PERKS[PerkType.WILDERNESS_CAMOUFLAGE],
            ],
            skills=[SkillType.PERCEPTION],
        )
    ),
    RaceType.DROW: ELF.model_copy(
        update=dict(
            name=RaceType.DROW,
            description="You are a drow, a dark elf who lives in the Underdark. You worship the spider goddess Lolth",
            charisma_bonus=1,
            weapon_proficiencies=[
                WeaponType.RAPIER,
                WeaponType.SHORTSWORD,
                WeaponType.HAND_CROSSBOW,
            ],
            perks=[
                PERKS[PerkType.PERFECT_NIGHT_VISION],
                PERKS[PerkType.FEY_ANCESTRY],
                PERKS[PerkType.SUNLIGHT_SENSITIVITY],
                PERKS[PerkType.DROW_MAGIC],
            ],
            skills=[SkillType.PERCEPTION],
        )
    ),
}
