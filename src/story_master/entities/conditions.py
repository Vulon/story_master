from enum import StrEnum

from pydantic import BaseModel


class ConditionType(StrEnum):
    UNCONSCIOUS = "unconscious"
    SCARED = "scared"
    INVISIBLE = "invisible"
    INCAPACITATED = "incapacitated"
    DEAFENED = "deafened"
    PETRIFIED = "petrified"
    RESTRAINED = "restrained"
    BLINDED = "blinded"
    POISONED = "poisoned"
    EXHAUSTION = "exhaustion"
    CHARMED = "charmed"
    STUNNED = "stunned"
    PARALYZED = "paralyzed"
    PRONE = "prone"
    GRAPPLED = "grappled"
    ENRAGED = "enraged"
    RECLESS_ATTACK_USED = "reckless attack used"
    FRENZIED = "frenzied"


class Condition(BaseModel):
    name: ConditionType
    description: str


CONDITIONS = {
    ConditionType.UNCONSCIOUS: Condition(
        name=ConditionType.UNCONSCIOUS,
        description="""
        • An unconscious creature is incapacitated (see the condition), can't move or speak, and is unaware of its surroundings.
        • The creature drops whatever it's holding and falls prone.
        • The creature automatically fails Strength and Dexterity saving throws.
        """,
    ),
    ConditionType.SCARED: Condition(
        name=ConditionType.SCARED,
        description="""
        • A frightened creature has disadvantage on ability checks and attack rolls while the source of its fear is within line of sight.
        • The creature can't willingly move closer to the source of its fear.
        """,
    ),
    ConditionType.DEAFENED: Condition(
        name=ConditionType.DEAFENED,
        description="""
        • A deafened creature can't hear and automatically fails any ability check that requires hearing.
        """,
    ),
    ConditionType.INVISIBLE: Condition(
        name=ConditionType.INVISIBLE,
        description="""
        • An invisible creature is impossible to see without the aid of magic or a special sense. For the purpose of hiding, the creature is heavily obscured. The creature's location can be detected by any noise it makes or any tracks it leaves.
        • Attack rolls against the creature have disadvantage, and the creature's attack rolls have advantage.
        """,
    ),
    ConditionType.INCAPACITATED: Condition(
        name=ConditionType.INCAPACITATED,
        description="""
        • An incapacitated creature can't take actions or reactions.
        """,
    ),
    ConditionType.ENRAGED: Condition(
        name=ConditionType.ENRAGED,
        description="""
        • An enraged creature has advantage on Strength checks and Strength saving throws.
        • When you make a melee weapon attack using Strength, you gain a +2 bonus to the damage roll.
        • You have resistance to bludgeoning, piercing, and slashing damage.
        • You can't cast spells.
        Rage ends early if you are knocked unconscious or if your turn ends and you haven't attacked a hostile creature since your last turn or taken damage since then.
        """,
    ),
    ConditionType.RECLESS_ATTACK_USED: Condition(
        name=ConditionType.RECLESS_ATTACK_USED,
        description="""
        You have used your reckless attack this turn.
        You have an advantage on melee weapon attack rolls using Strength during this turn, but attack rolls against you have advantage until the start of your next turn.
        """,
    ),
    ConditionType.FRENZIED: Condition(
        name=ConditionType.FRENZIED,
        description="""
        A frenzied creature is in a state of intense rage, allowing them to make a single melee weapon attack as a bonus action on each of their turns. However, when their rage ends, they suffer one level of exhaustion.
        """,
    ),
}
