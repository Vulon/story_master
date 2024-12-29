from pydantic import BaseModel

from story_master.entities.classes import Class
from story_master.entities.races import Race
from story_master.entities.background import Background
from enum import StrEnum
from story_master.entities.alignment import AlignmentType


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


GENDERS = [Gender.MALE, Gender.FEMALE, Gender.OTHER]


class Character(BaseModel):
    name: str
    sex: Gender
    age: int
    alignment: AlignmentType

    strength: int
    agility: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

    race: Race
    klass: Class
    background: Background

    level: int = 1
    experience: int = 0

    traits: list[str]
    ideal: str
    bond: str
    flaw: str

    money: float = 0


def calculate_bonus_from_characteristics(value: int) -> int:
    if value < 2:
        return -5
    if value > 39:
        return +10
    return (value - 10) // 2


def calculate_mastery_from_level(level: int) -> int:
    return (level - 1) // 4 + 2


def calculate_experience_to_next_level(level: int) -> int:
    # TODO: Implement a better formula
    return level * 1000
