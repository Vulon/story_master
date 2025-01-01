from enum import StrEnum

from pydantic import BaseModel

from story_master.entities.alignment import AlignmentType
from story_master.entities.background import Background
from story_master.entities.characteristics import (
    SKILL_CONDITIONS,
    CharacteristicType,
    SkillType,
)
from story_master.entities.classes import Class
from story_master.entities.items import Armor, Instrument, Item, WeaponType
from story_master.entities.perks import Perk
from story_master.entities.races import Race


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

    max_health: int
    current_health: int

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

    saving_throws: list[CharacteristicType]
    armor_proficiencies: list[Armor]
    weapon_proficiencies: list[WeaponType]
    skills: list[SkillType]
    items: list[Item]
    tool_proficiencies: list[Instrument]
    perks: list[Perk]

    money: float = 0

    def get_description(self) -> str:
        lines = [
            f"Name: {self.name}",
            f"Sex: {self.sex}",
            f"Age: {self.age}",
            f"Alignment: {self.alignment}",
            f"Health: {self.current_health}/{self.max_health}",
            f"Race: <Race>{self.race.get_shorter_description()}</Race>",
            f"Class: {self.klass.get_short_class_description()}",
            f"Background: <Background>{self.background.get_description()}</Background>",
            f"Level: {self.level}",
            f"Armor proficiencies: <Armor>{'; '.join([str(armor_category.name) for armor_category in self.armor_proficiencies])}</Armor>",
            f"Weapon proficiencies: <Weapons>{'; '.join([str(weapon.value) for weapon in self.weapon_proficiencies])}</Weapons>",
            f"Skills: <Skills>{'; '.join([f'{skill.value}: {SKILL_CONDITIONS[skill]}' for skill in self.skills])}</Skills>",
            f"Items: <Items>{'; '.join([item.name for item in self.items])}</Items>",
            f"Tool proficiencies: <Tools>{'; '.join([tool.get_full_description() for tool in self.tool_proficiencies])}</Tools>",
            f"Money: {self.money}",
            f"Perks: <Perks>{'; '.join([perk.get_full_description() for perk in self.perks])}</Perks>",
        ]
        return "\n".join(lines)


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
