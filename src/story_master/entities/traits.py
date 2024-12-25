from enum import StrEnum
from story_master.entities.perks import Perk
from pydantic import BaseModel

class TraitType(StrEnum):
    ARTISTIC = "Artistic"
    ATHLETIC = "Athletic"
    VIGILANT = "Vigilant"


class Trait(Perk):
    name: TraitType

TRAITS = {
    TraitType.ARTISTIC: Trait(
        name=TraitType.ARTISTIC,
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
    TraitType.ATHLETIC: Trait(
        name=TraitType.ATHLETIC,
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
    TraitType.VIGILANT: Trait(
        name=TraitType.VIGILANT,
        description=(
            "You are always ready for danger and gain the following benefits:\n\n"
            "• You gain a +5 bonus to initiative checks.\n"
            "• You can't be surprised while you are conscious.\n"
            "• Other creatures don't gain advantage on attack rolls against you as a result of being unseen by you."
        ),
        fight=True,
        exploration=True,
    )

}