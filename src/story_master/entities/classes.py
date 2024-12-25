from enum import StrEnum
from pydantic import BaseModel
from story_master.entities.characteristics import CharacteristicType
from story_master.entities.items import (
    ArmorType,
    WeaponType,
    WAR_WEAPONS,
    SIMPLE_WEAPONS,
    ArmorCategory,
)
from story_master.entities.perks import Perk


class ClassType(StrEnum):
    BARBARIAN = "Barbarian"
    BARD = "Bard"


class Class(BaseModel):
    name: ClassType
    health_dice: int
    main_characteristics: list[CharacteristicType]
    saving_throws: list[CharacteristicType]
    armor_proficiencies: list[ArmorType]
    weapon_proficiencies: list[WeaponType]
    perks: list[Perk]
    starting_money: float


class Barbarian(BaseModel):
    name = ClassType.BARBARIAN
    health_dice = 12
    main_characteristics = [CharacteristicType.STRENGTH]
    saving_throws = [CharacteristicType.STRENGTH, CharacteristicType.CONSTITUTION]
    armor_proficiencies = [
        ArmorCategory.LIGHT_ARMOR,
        ArmorCategory.MEDIUM_ARMOR,
        ArmorCategory.SHIELD,
    ]
    weapon_proficiencies = WAR_WEAPONS + SIMPLE_WEAPONS
    rage_uses: int
    starting_money = 40

    def get_mastery_bonus(self, level: int) -> int:
        return (level - 1) // 4 + 2

    def get_max_rage_uses(self, level: int) -> int:
        if level < 3:
            return 2
        if level < 6:
            return 3
        if level < 12:
            return 4
        if level < 17:
            return 5
        if level < 20:
            return 6
        return 10

    def get_rage_damage_bonus(self, level: int) -> int:
        if level < 9:
            return 2
        if level < 16:
            return 3
        return 4

    def get_perks(self, level: int) -> list[Perk]:
        perks = []
        if level > 0:
            perks += []
