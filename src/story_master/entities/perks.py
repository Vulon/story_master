from enum import StrEnum

from pydantic import BaseModel


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
    FRENZY = "frenzy"
    FAST_MOVEMENT = "fast movement"
    EXTRA_ATTACK = "extra attack"
    FEROCIOUS_INSTINCT = "ferocious instinct"
    BRUTAL_CRITICAL = "brutal critical"
    RELENTLESS_RAGE = "relentless rage"
    PERSISTENT_RAGE = "persistent rage"
    INDOMITABLE_MIGHT = "indomitable might"
    PRIMAL_CHAMPION = "primal champion"


class Perk(BaseModel):
    name: PerkType
    description: str
    fight: bool = False
    social: bool = False
    exploration: bool = False
    level_up: bool = False

    def get_full_description(self) -> str:
        return f"<Perk>{self.name}: {self.description}</Perk>"


PERKS = {
    PerkType.NIGHT_VISION: Perk(
        name=PerkType.NIGHT_VISION,
        description="This character can see in the dark",
        exploration=True,
    ),
    PerkType.PERFECT_NIGHT_VISION: Perk(
        name=PerkType.PERFECT_NIGHT_VISION,
        description="This character can see in the dark as if it was daylight",
        exploration=True,
    ),
    PerkType.DWARVEN_RESILIENCE: Perk(
        name=PerkType.DWARVEN_RESILIENCE,
        description="You have advantage on saving throws against poison, and you have resistance against poison damage",
        fight=True,
    ),
    PerkType.STONECUNNING: Perk(
        name=PerkType.STONECUNNING,
        description="Whenever you make an Intelligence (History) check related to the origin of stonework, you are considered proficient in the History skill and add double your proficiency bonus to the check",
        exploration=True,
    ),
    PerkType.FEY_ANCESTRY: Perk(
        name=PerkType.FEY_ANCESTRY,
        description="You have advantage on saving throws against being charmed, and magic can't put you to sleep",
        social=True,
    ),
    PerkType.TRANCE: Perk(
        name=PerkType.TRANCE,
        description="You don't need to sleep. Instead, you meditate deeply, remaining semiconscious, for 4 hours a day",
        exploration=True,
    ),
    PerkType.DWARVEN_TOUGHNESS: Perk(
        name=PerkType.DWARVEN_TOUGHNESS,
        description="Your hit point maximum increases by 1, and it increases by 1 every time you gain a level",
        level_up=True,
    ),
    PerkType.WILDERNESS_CAMOUFLAGE: Perk(
        name=PerkType.WILDERNESS_CAMOUFLAGE,
        description="You can attempt to hide even when you are only lightly obscured by foliage, heavy rain, falling snow, mist, and other natural phenomena.",
        exploration=True,
    ),
    PerkType.SUNLIGHT_SENSITIVITY: Perk(
        name=PerkType.SUNLIGHT_SENSITIVITY,
        description="You have disadvantage on attack rolls and on Wisdom (Perception) checks that rely on sight when you, the target of your attack, or whatever you are trying to perceive is in direct sunlight",
        fight=True,
        exploration=True,
    ),
    PerkType.DROW_MAGIC: Perk(
        name=PerkType.DROW_MAGIC,
        description="You know the dancing lights cantrip. When you reach 3rd level, you can cast the faerie fire spell once per day. When you reach 5th level, you can also cast the darkness spell once per day. Charisma is your spellcasting ability for these spells",
        level_up=True,
    ),
    PerkType.UNARMORED_DEFENSE: Perk(
        name=PerkType.UNARMORED_DEFENSE,
        description="If you are not wearing armor, your Armor Class equals 10 + your Dexterity modifier + your Constitution modifier. You can use a shield and still gain this benefit.",
        exploration=True,
        fight=True,
        level_up=True,
    ),
    PerkType.RAGE: Perk(
        name=PerkType.RAGE,
        description="""
        In battle, you fight with primal ferocity. On your turn, you can enter a rage as a bonus action.                
        """,
        fight=True,
    ),
    PerkType.RECKLESS_ATTACK: Perk(
        name=PerkType.RECKLESS_ATTACK,
        description="""
        When you make your first attack on your turn, you can decide to attack recklessly.
        Doing so gives you advantage on melee weapon attack rolls using Strength during this turn, but attack rolls against you have advantage until your next turn.
        """,
        fight=True,
    ),
    PerkType.DANGER_SENSE: Perk(
        name=PerkType.DANGER_SENSE,
        description="""
        You gain an uncanny sense of when things nearby aren't as they should be, giving you an edge when you dodge away from danger.
        You have advantage on Dexterity saving throws against effects that you can see, such as traps and spells. To gain this benefit, you can't be blinded, deafened, or incapacitated.
        """,
        fight=True,
        exploration=True,
    ),
    PerkType.FRENZY: Perk(
        name=PerkType.FRENZY,
        description="""
        while you are raging, you can go into a frenzy.
        If you do so, for the duration of your rage, you can make a single melee weapon attack as a bonus action on each of your turns after this one.
        When your rage ends, you suffer one level of exhaustion
        """,
        fight=True,
    ),
}
