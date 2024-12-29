from enum import StrEnum
from story_master.entities.perks import Perk


class FeatType(StrEnum):
    ARTISTIC = "Actor"
    ATHLETIC = "Athlete"
    VIGILANT = "Alert"
    WAR_CASTER = "War Caster"
    GRAPPLER = "Grappler"
    LUCKY = "Lucky"
    MOUNTED_COMBATANT = "Mounted Combatant"
    OBSERVANT = "Observant"
    MARTIAL_ADEPT = "Martial Adept"
    INSPIRING_LEADER = "Inspiring Leader"
    DUAL_WIELDER = "Dual Wielder"
    SAVAGE_ATTACKER = "Savage Attacker"
    TAVERN_BRAWLER = "Tavern Brawler"
    LIGHTLY_ARMORED = "Lightly Armored"
    MODERATELY_ARMORED = "Moderately Armored"
    HEAVILY_ARMORED = "Heavily Armored"
    DUNGEON_DELVER = "Dungeon Delver"
    TOUGH = "Tough"
    HEALER = "Healer"
    GREAT_WEAPON_MASTER = "Great Weapon Master"
    POLEARM_MASTER = "Polearm Master"
    WEAPON_MASTER = "Weapon Master"
    MEDIUM_ARMOR_MASTER = "Medium Armor Master"
    HEAVY_ARMOR_MASTER = "Heavy Armor Master"
    SHIELD_MASTER = "Shield Master"
    SPELL_SNIPER = "Spell Sniper"
    SHARPSHOOTER = "Sharpshooter"
    CHARGER = "Charger"
    DEFENSIVE_DUELIST = "Defensive Duelist"
    SKILLED = "Skilled"
    KEEN_MIND = "Keen Mind"
    MOBILE = "Mobile"
    MAGIC_INITIATE = "Magic Initiate"
    SKULKER = "Skulker"
    RITUAL_CASTER = "Ritual Caster"
    ELEMENTAL_ADEPT = "Elemental Adept"
    DURABLE = "Durable"
    SENTINEL = "Sentinel"
    MAGE_SLAYER = "Mage Slayer"
    RESILIENT = "Resilient"
    CROSSBOW_EXPERT = "Crossbow Expert"
    LINGUIST = "Linguist"


class Feat(Perk):
    name: FeatType


TRAITS = {
    FeatType.ARTISTIC: Feat(
        name=FeatType.ARTISTIC,
        description=(
            "Having learned the art of theater and mimicry, you gain the following benefits:\n\n"
            "• Increase your Charisma score by 1, up to a maximum of 20.\n"
            "• You have advantage on Charisma (Performance) and Charisma (Deception) checks when "
            "trying to pass yourself off as someone else.\n"
            "• You can mimic the speech of another person or the sounds made by other creatures. "
            "You must have heard the person speaking, or heard the creature make the sound, for at least 1 minute. "
            "A successful Wisdom (Insight) check contested by your Charisma (Deception) check allows a listener "
            "to determine that the effect is faked."
        ),
        social=True,
        level_up=True,
    ),
    FeatType.ATHLETIC: Feat(
        name=FeatType.ATHLETIC,
        description=(
            "You have undergone intensive physical training and gain the following benefits:\n\n"
            "• Increase your Strength or Dexterity score by 1, up to a maximum of 20.\n"
            "• If you are prone, standing up uses only 5 feet of movement.\n"
            "• Climbing doesn't cost you extra movement.\n"
            "• You can make a running long jump or a running high jump after moving only 5 feet on foot, rather than 10 feet."
        ),
        exploration=True,
        level_up=True,
    ),
    FeatType.VIGILANT: Feat(
        name=FeatType.VIGILANT,
        description=(
            "You are always ready for danger and gain the following benefits:\n\n"
            "• You gain a +5 bonus to initiative checks.\n"
            "• You can't be surprised while you are conscious.\n"
            "• Other creatures don't gain advantage on attack rolls against you as a result of being unseen by you."
        ),
        fight=True,
        exploration=True,
    ),
}
