from pydantic import BaseModel
from enum import StrEnum


class PerkType(StrEnum):
    NIGHT_VISION = "night vision"
    PERFECT_NIGHT_VISION = "perfect night vision"
    DWARVEN_RESILIENCE = "dwarven resilience"
    STONECUNNING = "stonecunning"
    PERCEPTION = "perception"
    FEY_ANCESTRY = "fey ancestry"
    TRANCE = "trance"
    DWARVEN_TOUGHNESS = "dwarven toughness"
    WILDERNESS_CAMOUFLAGE = "wilderness camouflage"
    SUNLIGHT_SENSITIVITY = "sunlight sensitivity"
    DROW_MAGIC = "drow magic"
    UNARMORED_DEFENSE = "unarmored defense"
    RAGE = "rage"
    RECKLESS_ATTACK = "reckless attack"
    DANGER_SENSE = "danger sense"
    PATH_OF_THE_BERSERKER = "path of the berserker"
    ABILITY_SCORE_IMPROVEMENT = "ability score improvement"
    FAST_MOVEMENT = "fast movement"
    EXTRA_ATTACK = "extra attack"
    FEROCIOUS_INSTINCT = "ferocious instinct"
    BRUTAL_CRITICAL = "brutal critical"
    RELENTLESS_RAGE = "relentless rage"
    PERSISTENT_RAGE = "persistent rage"
    INDOMITABLE_MIGHT = "indomitable might"
    PRIMAL_CHAMPION = "primal champion"
    SHELTER_OF_THE_FAITHFUL = "shelter of the faithful"


class Perk(BaseModel):
    name: PerkType
    description: str
    fight: bool = False
    social: bool = False
    exploration: bool = False
    level_up: bool = False


PERKS = {
    PerkType.NIGHT_VISION: Perk(
        name="night vision",
        description="This character can see in the dark",
        exploration=True,
    ),
    PerkType.PERFECT_NIGHT_VISION: Perk(
        name="perfect night vision",
        description="This character can see in the dark as if it was daylight",
        exploration=True,
    ),
    PerkType.DWARVEN_RESILIENCE: Perk(
        name="dwarven resilience",
        description="You have advantage on saving throws against poison, and you have resistance against poison damage",
        fight=True,
    ),
    PerkType.STONECUNNING: Perk(
        name="stonecunning",
        description="Whenever you make an Intelligence (History) check related to the origin of stonework, you are considered proficient in the History skill and add double your proficiency bonus to the check",
        exploration=True,
    ),
    PerkType.PERCEPTION: Perk(
        name="perception",
        description="You have advantage on perception checks",
        exploration=True,
    ),
    PerkType.FEY_ANCESTRY: Perk(
        name="fey ancestry",
        description="You have advantage on saving throws against being charmed, and magic can't put you to sleep",
        social=True,
    ),
    PerkType.TRANCE: Perk(
        name="trance",
        description="You don't need to sleep. Instead, you meditate deeply, remaining semiconscious, for 4 hours a day",
        exploration=True,
    ),
    PerkType.DWARVEN_TOUGHNESS: Perk(
        name="dwarven toughness",
        description="Your hit point maximum increases by 1, and it increases by 1 every time you gain a level",
        level_up=True,
    ),
    PerkType.WILDERNESS_CAMOUFLAGE: Perk(
        name="wilderness camouflage",
        description="You can attempt to hide even when you are only lightly obscured by foliage, heavy rain, falling snow, mist, and other natural phenomena.",
        exploration=True,
    ),
    PerkType.SUNLIGHT_SENSITIVITY: Perk(
        name="sunlight sensitivity",
        description="You have disadvantage on attack rolls and on Wisdom (Perception) checks that rely on sight when you, the target of your attack, or whatever you are trying to perceive is in direct sunlight",
        fight=True,
        exploration=True,
    ),
    PerkType.DROW_MAGIC: Perk(
        name="drow magic",
        description="You know the dancing lights cantrip. When you reach 3rd level, you can cast the faerie fire spell once per day. When you reach 5th level, you can also cast the darkness spell once per day. Charisma is your spellcasting ability for these spells",
        level_up=True,
    ),
    PerkType.SHELTER_OF_THE_FAITHFUL: Perk(
        name="shelter of the faithful",
        description="You and your companions can expect free healing and care at temples, shrines, and other established places of your faith. You must provide any material components needed for spells. Those who share your faith will support you (but only you) at a modest lifestyle. You might have ties to a specific temple dedicated to your chosen deity or pantheon and have a residence there. While near your temple, you can call upon the priests for assistance, provided it does not endanger them.",
        social=True,
        exploration=True,
    ),
}
