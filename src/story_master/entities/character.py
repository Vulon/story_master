from enum import StrEnum
from typing import Literal
from abc import ABC

from pydantic import BaseModel


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


GENDERS = [Gender.MALE, Gender.FEMALE, Gender.OTHER]


class CharacterType(StrEnum):
    SETTLER = "settler"
    # Monsters, animals, etc.
    ANIMAL = "animal"


class Character(BaseModel, ABC):
    type: CharacterType
    name: str
    appearance: str
    gender: Gender
    age: int

    def get_self_description(self) -> str:
        pass

    def get_external_description(self) -> str:
        pass

class Settler(Character):
    type: Literal[CharacterType.SETTLER] = CharacterType.SETTLER

    def get_self_description(self) -> str:
        lines = [
            "<Settler>",
            f"Name: {self.name}",
            f"Appearance: {self.appearance}",
            f"Gender: {self.gender}",
            f"Age: {self.age}",
            "</Settler>",
        ]
        return " ".join(lines)

    def get_external_description(self) -> str:
        lines = [
            "<Settler>",
            f"Appearance: {self.appearance}",
            f"Gender: {self.gender}",
            "</Settler>",
        ]
        return " ".join(lines)


class Animal(Character):
    type: Literal[CharacterType.ANIMAL] = CharacterType.ANIMAL

    def get_self_description(self) -> str:
        lines = [
            "<Animal>",
            f"Name: {self.name}",
            f"Appearance: {self.appearance}",
            f"Gender: {self.gender}",
            f"Age: {self.age}",
            "</Animal>",
        ]
        return " ".join(lines)

    def get_external_description(self) -> str:
        lines = [
            "<Animal>",
            f"Appearance: {self.appearance}",
            f"Gender: {self.gender}",
            "</Animal>",
        ]
        return " ".join(lines)


ANY_CHARACTER = Settler | Animal

CHARACTER_TYPE_TABLE = {
    CharacterType.SETTLER: Settler,
    CharacterType.ANIMAL: Animal,
}

