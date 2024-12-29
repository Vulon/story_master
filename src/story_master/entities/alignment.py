from enum import StrEnum


class AlignmentType(StrEnum):
    LAWFUL_GOOD = "Lawful Good"
    NEUTRAL_GOOD = "Neutral Good"
    CHAOTIC_GOOD = "Chaotic Good"
    LAWFUL_NEUTRAL = "Lawful Neutral"
    TRUE_NEUTRAL = "True Neutral"
    CHAOTIC_NEUTRAL = "Chaotic Neutral"
    LAWFUL_EVIL = "Lawful Evil"
    NEUTRAL_EVIL = "Neutral Evil"
    CHAOTIC_EVIL = "Chaotic Evil"


ALIGNMENTS = [
    AlignmentType.LAWFUL_GOOD,
    AlignmentType.NEUTRAL_GOOD,
    AlignmentType.CHAOTIC_GOOD,
    AlignmentType.LAWFUL_NEUTRAL,
    AlignmentType.TRUE_NEUTRAL,
    AlignmentType.CHAOTIC_NEUTRAL,
    AlignmentType.LAWFUL_EVIL,
    AlignmentType.NEUTRAL_EVIL,
    AlignmentType.CHAOTIC_EVIL,
]
