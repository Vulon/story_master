from enum import StrEnum
from typing import Literal

from pydantic import BaseModel

from story_master.entities.characteristics import CharacteristicType, SkillType
from story_master.entities.conditions import ConditionType
from story_master.entities.items import (
    ARMORS,
    EXPLORER_BUNDLE,
    LIGHT_ARMORS,
    MEDIUM_ARMORS,
    SIMPLE_WEAPONS,
    WAR_WEAPONS,
    WEAPONS,
    Armor,
    ArmorCategory,
    ArmorType,
    Item,
    WeaponType,
    EQUIPMENT,
    EquipmentType,
)
from story_master.entities.perks import PERKS, Perk, PerkType
from story_master.utils.selection import SomeOf


class AdventurerClassType(StrEnum):
    BARBARIAN = "Barbarian"
    BARD = "Bard"


class CivilianClassType(StrEnum):
    COMMONER = "Commoner"


class CreatureClassType(StrEnum):
    MONSTER = "Monster"
    ANIMAL = "Animal"


class PerkException(Exception):
    pass


(15, 14, 13, 12, 10, 8)


class BaseClass(BaseModel):
    name: AdventurerClassType | CivilianClassType | CreatureClassType
    health_dice: int
    base_strength: int
    base_agility: int
    base_constitution: int
    base_intelligence: int
    base_wisdom: int
    base_charisma: int

    def get_short_class_description(self) -> str:
        pass


class CivilianClass(BaseClass):
    name: Literal[CivilianClassType.COMMONER] = CivilianClassType.COMMONER
    health_dice: int = 6
    base_strength: int = 10
    base_agility: int = 10
    base_constitution: int = 10
    base_intelligence: int = 10
    base_wisdom: int = 10
    base_charisma: int = 10

    # TODO: Add more starting items
    starting_items: list[Item] = [
        EQUIPMENT[EquipmentType.COMMON_CLOTHES],
    ]

    def get_short_class_description(self) -> str:
        return "A common person with no combat skills"


class AdventurerClass(BaseClass):
    name: AdventurerClassType

    main_characteristics: list[CharacteristicType]
    saving_throws: list[CharacteristicType]
    armor_proficiencies: list[Armor]
    weapon_proficiencies: list[WeaponType]
    skills: list[SkillType] | SomeOf
    starting_money: float
    starting_items: list[Item]
    active_conditions: list[ConditionType] = []

    def get_mastery_bonus(self, level: int) -> int:
        pass

    def get_perks(self, level: int) -> list[Perk]:
        pass

    def use_long_rest(self, level: int) -> None:
        pass

    def activate_perk(self, perk: PerkType) -> None:
        pass

    def disable_perk(self, perk: PerkType) -> None:
        pass

    def get_stats_increase(self, level: int) -> int:
        pass

    def get_short_class_description(self) -> str:
        pass


class CreatureClass(BaseClass):
    pass


class Barbarian(AdventurerClass):
    name: Literal[AdventurerClassType.BARBARIAN] = AdventurerClassType.BARBARIAN
    health_dice: int = 12
    is_enraged: bool = False
    is_frenzied: bool = False
    rage_uses_left: int = 0

    base_strength: int = 15
    base_agility: int = 13
    base_constitution: int = 14
    base_intelligence: int = 8
    base_wisdom: int = 12
    base_charisma: int = 10

    main_characteristics: list[CharacteristicType] = [CharacteristicType.STRENGTH]
    saving_throws: list[CharacteristicType] = [
        CharacteristicType.STRENGTH,
        CharacteristicType.CONSTITUTION,
    ]
    armor_proficiencies: list[ArmorCategory] = (
        LIGHT_ARMORS + MEDIUM_ARMORS + [ARMORS[ArmorType.SHIELD]]
    )
    weapon_proficiencies: list[WeaponType] = WAR_WEAPONS + SIMPLE_WEAPONS

    starting_money: float = 40
    skills: list[SkillType] | SomeOf = SomeOf(
        count=2,
        items=[
            SkillType.ATHLETICS,
            SkillType.PERCEPTION,
            SkillType.SURVIVAL,
            SkillType.INTIMIDATION,
            SkillType.NATURE,
            SkillType.ANIMAL_HANDLING,
        ],
    )

    starting_items: list[Item] = [
        WEAPONS[WeaponType.GREATAXE],
        WEAPONS[WeaponType.HANDAXE],
        WEAPONS[WeaponType.HANDAXE],
        WEAPONS[WeaponType.JAVELIN],
        WEAPONS[WeaponType.JAVELIN],
        WEAPONS[WeaponType.JAVELIN],
        WEAPONS[WeaponType.JAVELIN],
    ] + EXPLORER_BUNDLE

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

    def use_long_rest(self, level: int) -> None:
        self.rage_uses_left = self.get_max_rage_uses(level)
        self.is_enraged = False

    def activate_perk(self, perk: PerkType) -> None:
        if perk == PerkType.RAGE:
            if self.rage_uses_left <= 0:
                raise PerkException("No more rage uses left")
            if self.is_enraged:
                raise PerkException("Already enraged")
            self.is_enraged = True
            self.rage_uses_left -= 1
            self.active_conditions.append(ConditionType.ENRAGED)
        if perk == PerkType.RECKLESS_ATTACK:
            if ConditionType.RECLESS_ATTACK_USED in self.active_conditions:
                raise PerkException("Reckless attack already used")
            self.active_conditions.append(ConditionType.RECLESS_ATTACK_USED)
        if perk == PerkType.FRENZY:
            self.is_frenzied = True
            self.active_conditions.append(ConditionType.FRENZIED)

    def disable_perk(self, perk: PerkType) -> None:
        if perk == PerkType.RAGE:
            self.is_enraged = False
            self.active_conditions.remove(ConditionType.ENRAGED)
            if self.is_frenzied:
                self.is_frenzied = False
                self.active_conditions.remove(ConditionType.FRENZIED)
        if perk == PerkType.FRENZY:
            self.is_frenzied = False
            self.active_conditions.remove(ConditionType.FRENZIED)
        if perk == PerkType.RECKLESS_ATTACK:
            self.active_conditions.remove(ConditionType.RECLESS_ATTACK_USED)

    def get_perks(self, level: int) -> list[Perk]:
        perks = []
        if level > 0:
            perks += [PERKS[PerkType.UNARMORED_DEFENSE], PERKS[PerkType.RAGE]]
        if level > 1:
            perks += [PERKS[PerkType.RECKLESS_ATTACK], PERKS[PerkType.DANGER_SENSE]]
        if level > 2:
            perks += [PERKS[PerkType.FRENZY]]
        return perks

    def get_stats_increase(self, level: int) -> int:
        # Levels at which stats increase
        stat_increase_levels = [4, 8, 12, 16, 19]
        # Calculate the total stat increases
        total_increases = sum(
            2 for threshold_level in stat_increase_levels if level >= threshold_level
        )
        return total_increases

    def get_short_class_description(self) -> str:
        return "A fierce warrior of primitive background who can enter a battle rage"


# TODO: Implement Totem Warrior for Barbarian


CLASSES = {AdventurerClassType.BARBARIAN: Barbarian()}
