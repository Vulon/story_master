from enum import StrEnum
from typing import Literal
from abc import ABC, abstractmethod

from pydantic import BaseModel

from story_master.entities.alignment import AlignmentType
from story_master.entities.background import Background
from story_master.entities.characteristics import (
    SKILL_CONDITIONS,
    CharacteristicType,
    SkillType,
)
from story_master.entities.classes import AdventurerClass, CivilianClass, CreatureClass
from story_master.entities.items import Armor, Instrument, WeaponType
from story_master.entities.items.items import ItemStack
from story_master.entities.perks import Perk
from story_master.entities.races import Race


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


GENDERS = [Gender.MALE, Gender.FEMALE, Gender.OTHER]


class CharacterType(StrEnum):
    ADVENTURER = "adventurer"
    # Common people with no combat skills including peasants, farmers, townsfolk, etc.
    COMMONER = "commoner"
    MERCHANT = "merchant"
    # Monsters, animals, etc.
    CREATURE = "creature"


class Character(BaseModel, ABC):
    type: CharacterType
    name: str
    sex: Gender
    age: int
    alignment: AlignmentType

    max_health: int
    current_health: int
    level: int = 1
    experience: int = 0

    race: Race

    strength: int
    agility: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

    @abstractmethod
    def get_description(self) -> str:
        pass


class Adventurer(Character):
    type: Literal[CharacterType.ADVENTURER]
    klass: AdventurerClass
    background: Background
    saving_throws: list[CharacteristicType]
    perks: list[Perk]
    armor_proficiencies: list[Armor]
    weapon_proficiencies: list[WeaponType]
    skills: list[SkillType]
    items: dict[str, ItemStack]
    tool_proficiencies: list[Instrument]
    money: float = 0

    def get_description(self) -> str:
        lines = [
            "<Adventurer>",
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
            f"Items: <Items>{'; '.join([f'{stack.item.name} x {stack.quantity}' for stack in self.items.values()])}</Items>",
            f"Tool proficiencies: <Tools>{'; '.join([tool.get_full_description() for tool in self.tool_proficiencies])}</Tools>",
            f"Money: {self.money}",
            f"Perks: <Perks>{'; '.join([perk.get_full_description() for perk in self.perks])}</Perks>",
            "</Adventurer>",
        ]
        return "\n".join(lines)


class Commoner(Character):
    type: Literal[CharacterType.COMMONER]
    klass: CivilianClass
    money: float = 0
    items: dict[str, ItemStack]
    tool_proficiencies: list[Instrument]

    def get_description(self) -> str:
        lines = [
            "<Commoner>",
            f"Name: {self.name}",
            f"Sex: {self.sex}",
            f"Age: {self.age}",
            f"Alignment: {self.alignment}",
            f"Health: {self.current_health}/{self.max_health}",
            f"Race: <Race>{self.race.get_shorter_description()}</Race>",
            f"Class: {self.klass.get_short_class_description()}",
            f"Level: {self.level}",
            f"Items: <Items>{'; '.join([f'{stack.item.name} x {stack.quantity}' for stack in self.items.values()])}</Items>",
            f"Tool proficiencies: <Tools>{'; '.join([tool.get_full_description() for tool in self.tool_proficiencies])}</Tools>",
            f"Money: {self.money}",
            "</Commoner>",
        ]
        return "\n".join(lines)


class Merchant(Character):
    type: Literal[CharacterType.MERCHANT]
    klass: CivilianClass
    money: float = 0
    items: dict[str, ItemStack]
    stock: dict[str, ItemStack]

    def get_description(self) -> str:
        lines = [
            "<Merchant>",
            f"Name: {self.name}",
            f"Sex: {self.sex}",
            f"Age: {self.age}",
            f"Alignment: {self.alignment}",
            f"Health: {self.current_health}/{self.max_health}",
            f"Race: <Race>{self.race.get_shorter_description()}</Race>",
            f"Class: {self.klass.get_short_class_description()}",
            f"Level: {self.level}",
            f"Items: <Items>{'; '.join([f'{stack.item.name} x {stack.quantity}' for stack in self.items.values()])}</Items>",
            f"Stock for sale: <Stock>{'; '.join([f'{stack.item.name} x {stack.quantity}' for stack in self.stock])}</Stock>",
            f"Money: {self.money}",
            "</Merchant>",
        ]
        return "\n".join(lines)


class Creature(Character):
    type: Literal[CharacterType.CREATURE]
    klass: CreatureClass
    saving_throws: list[CharacteristicType]
    perks: list[Perk]

    def get_description(self) -> str:
        lines = [
            "<Creature>",
            f"Name: {self.name}",
            f"Sex: {self.sex}",
            f"Age: {self.age}",
            f"Alignment: {self.alignment}",
            f"Health: {self.current_health}/{self.max_health}",
            f"Race: <Race>{self.race.get_shorter_description()}</Race>",
            f"Level: {self.level}",
            f"Perks: <Perks>{'; '.join([perk.get_full_description() for perk in self.perks])}</Perks>",
            "</Creature>",
        ]
        return "\n".join(lines)


ANY_CHARACTER = Adventurer | Commoner | Merchant | Creature

CHARACTER_TYPE_TABLE = {
    CharacterType.ADVENTURER: Adventurer,
    CharacterType.COMMONER: Commoner,
    CharacterType.MERCHANT: Merchant,
    CharacterType.CREATURE: Creature,
}


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
