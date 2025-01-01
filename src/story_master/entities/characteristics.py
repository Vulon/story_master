from enum import StrEnum
from typing import Literal

from pydantic import BaseModel


class CharacteristicType(StrEnum):
    STRENGTH = "Strength"
    DEXTERITY = "Dexterity"
    CONSTITUTION = "Constitution"
    INTELLIGENCE = "Intelligence"
    WISDOM = "Wisdom"
    CHARISMA = "Charisma"


class DamageType(StrEnum):
    BLUDGEONING = "Bludgeoning"
    PIERCING = "Piercing"
    SLASHING = "Slashing"
    RADIANT = "Radiant"
    ACID = "Acid"
    NECROTIC = "Necrotic"
    FIRE = "Fire"
    PSYCHIC = "Psychic"
    FORCE = "Force"
    COLD = "Cold"
    LIGHTNING = "Lightning"
    POISON = "Poison"


class Size(StrEnum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


SIZES = [Size.SMALL, Size.MEDIUM, Size.LARGE]


class SkillType(StrEnum):
    ACROBATICS = "Acrobatics"
    ANIMAL_HANDLING = "Animal Handling"
    ARCANA = "Arcana"
    ATHLETICS = "Athletics"
    DECEPTION = "Deception"
    HISTORY = "History"
    INSIGHT = "Insight"
    INTIMIDATION = "Intimidation"
    INVESTIGATION = "Investigation"
    MEDICINE = "Medicine"
    NATURE = "Nature"
    PERCEPTION = "Perception"
    PERFORMANCE = "Performance"
    PERSUASION = "Persuasion"
    RELIGION = "Religion"
    SLEIGHT_OF_HAND = "Sleight of Hand"
    STEALTH = "Stealth"
    SURVIVAL = "Survival"


SKILL_GROUPS = {
    CharacteristicType.STRENGTH: [SkillType.ATHLETICS],
    CharacteristicType.DEXTERITY: [
        SkillType.ACROBATICS,
        SkillType.SLEIGHT_OF_HAND,
        SkillType.STEALTH,
    ],
    CharacteristicType.CONSTITUTION: [],
    CharacteristicType.INTELLIGENCE: [
        SkillType.ARCANA,
        SkillType.HISTORY,
        SkillType.INVESTIGATION,
        SkillType.NATURE,
        SkillType.RELIGION,
    ],
    CharacteristicType.WISDOM: [
        SkillType.ANIMAL_HANDLING,
        SkillType.INSIGHT,
        SkillType.MEDICINE,
        SkillType.PERCEPTION,
        SkillType.SURVIVAL,
    ],
    CharacteristicType.CHARISMA: [
        SkillType.DECEPTION,
        SkillType.INTIMIDATION,
        SkillType.PERFORMANCE,
        SkillType.PERSUASION,
    ],
}

SKILL_CONDITIONS = {
    SkillType.ATHLETICS: """
    Athletics (Strength) checks cover climbing, jumping, and swimming situations such as:
    Climbing steep cliffs or maintaining grip when being shaken off
    Making long-distance jumps or performing mid-air maneuvers
    Swimming in rough waters, storms, or seaweed-filled areas, including when other creatures try to push you underwater or interfere with your swimming
    """,
    SkillType.ACROBATICS: """
    Dexterity (Acrobatics) checks involve maintaining balance in tricky situations, such as running on ice, walking a tightrope, or standing on a storm-tossed ship's deck.
    They can also be used for acrobatic feats like dives, flips, rolls, or tumbles.
    """,
    SkillType.SLEIGHT_OF_HAND: """
Dexterity (Sleight of Hand) checks cover actions like juggling, performing tricks, hiding objects on your person, picking pockets, or planting items on someone else.
    """,
    SkillType.STEALTH: """
Make a Dexterity (Stealth) check when trying to hide from enemies, sneak past guards, escape unnoticed, or approach someone quietly and unseen.
    """,
    SkillType.INVESTIGATION: """
    When you look for clues and make deductions based on them, you make an Intelligence (Investigation) check.
    You might deduce the location of a hidden object, determine what kind of weapon dealt a wound by its appearance, or identify the weakest point in a tunnel that could cause it to collapse.
    Examining ancient scrolls for hidden knowledge might also require an Intelligence (Investigation) check.
    """,
    SkillType.HISTORY: """
    An Intelligence (History) check determines your ability to recall knowledge about historical events, legendary people, ancient kingdoms, past disputes, recent wars, and lost civilizations.
    """,
    SkillType.ARCANA: """
    An Intelligence (Arcana) check determines your ability to recall knowledge about spells, magic items, eldritch symbols, magical traditions, the planes of existence, and the inhabitants of those planes.
    """,
    SkillType.NATURE: """
    An Intelligence (Nature) check determines your ability to recall knowledge about terrain, plants and animals, the weather, and natural cycles.
    """,
    SkillType.RELIGION: """
    An Intelligence (Religion) check determines your ability to recall knowledge about deities, rites and prayers, religious hierarchies, holy symbols, and the practices of secret cults.
    """,
    SkillType.INSIGHT: """
    An Wisdom (Insight) check determines your ability to determine the true intentions of a creature, such as when searching out a lie or predicting someone's next move.
    """,
    SkillType.MEDICINE: """
    An Wisdom (Medicine) check determines your ability to stabilize a dying companion or diagnose an illness.
    """,
    SkillType.PERCEPTION: """
    An Wisdom (Perception) check determines your ability to spot, hear, or otherwise detect the presence of something.
    It measures your general awareness of your surroundings and the keenness of your senses.
    """,
    SkillType.ANIMAL_HANDLING: """
    An Wisdom (Animal Handling) check determines your ability to calm a domesticated animal, keep a mount from getting spooked, or intuit an animal's intentions.
    """,
    SkillType.SURVIVAL: """
    An Wisdom (Survival) check determines your ability to follow tracks, hunt wild game, guide your group through frozen wastelands, identify signs that owlbears live nearby, predict the weather, or avoid quicksand and other natural hazards.
    """,
    SkillType.PERFORMANCE: """
    A Charisma (Performance) check determines your ability to delight an audience with music, dance, acting, storytelling, or some other form of entertainment.
    """,
    SkillType.INTIMIDATION: """
    A Charisma (Intimidation) check determines your ability to influence others through threats, hostile actions, and physical violence.
    """,
    SkillType.DECEPTION: """
    A Charisma (Deception) check determines your ability to convincingly hide the truth, either verbally or through your actions.
    This deception can encompass everything from misleading others through ambiguity to telling outright lies.
    Typical situations include:
    • Bluffing your way past a guard
    • Pretending to be someone you're not
    • Passing yourself off as a different
    """,
    SkillType.PERSUASION: """
    A Charisma (Persuasion) check determines your ability to influence others through negotiation, diplomacy, and leadership.
    """,
}

# Page 177


class Characteristic(BaseModel):
    name: CharacteristicType
    skill_proficiencies: list[SkillType]
    description: str

    def get_when_characteristic_can_be_used(self) -> str:
        pass

    def get_when_skill_can_be_used(self, skill: SkillType) -> str:
        pass

    def get_fight_impact(self) -> str:
        pass

    def get_social_impact(self) -> str:
        pass

    def get_exploration_impact(self) -> str:
        pass

    def get_stats_impact(self) -> str:
        pass


class Strength(Characteristic):
    name: Literal[CharacteristicType.STRENGTH] = CharacteristicType.STRENGTH
    skill_proficiencies: list[SkillType] = [SkillType.ATHLETICS]
    USE_CONDITION: str = """
Strength checks determine your ability to exert physical force - whether you're lifting, pushing, pulling, or breaking objects, as well as squeezing into tight spaces.
Common Strength checks include:
- Breaking down stuck or barred doors
- Breaking free from restraints
- Squeezing through narrow tunnels
- Holding onto moving vehicles
- Pushing over statues
- Preventing boulders from falling"""

    ATTACK_IMPACT: str = """
Your Strength modifier is added to attack rolls and damage when using melee weapons like maces, axes, or javelins.
Melee weapons are used for close combat attacks, and some can be thrown for ranged attacks."""

    WEIGHT_LIFTING: str = """
The Strength score determines the weight your character can carry, using the following terms:
Carrying Capacity: Your carrying capacity is equal to your Strength score multiplied by 15.
This is the weight (in pounds) that you can carry without being hindered.
It is usually sufficient, so most characters don't need to worry about it.
Pushing, Dragging, and Lifting: You can push, drag, or lift a weight (in pounds) up to twice your carrying capacity, which equals your Strength score multiplied by 30.
However, if you push or drag a weight exceeding your carrying capacity, your movement speed drops to 5 feet.
Size and Strength: Creatures of larger size categories can carry more weight, while Tiny creatures carry less.
For every size category above Medium, double the creature's carrying capacity and the weight it can push, drag, or lift.
For Tiny creatures, these values are halved"""

    def get_when_characteristic_can_be_used(self) -> str:
        return Strength.USE_CONDITION

    def get_when_skill_can_be_used(self, skill: SkillType) -> str:
        if skill == SkillType.ATHLETICS:
            return SKILL_CONDITIONS[skill]
        else:
            return None

    def get_fight_impact(self) -> str:
        return Strength.ATTACK_IMPACT

    def get_social_impact(self) -> str:
        return None

    def get_exploration_impact(self) -> str:
        return Strength.WEIGHT_LIFTING

    def get_stats_impact(self) -> str:
        return Strength.WEIGHT_LIFTING


class Dexterity(Characteristic):
    name: Literal[CharacteristicType.DEXTERITY] = CharacteristicType.DEXTERITY
    skill_proficiencies: list[SkillType] = [
        SkillType.ACROBATICS,
        SkillType.SLEIGHT_OF_HAND,
        SkillType.STEALTH,
    ]
    USE_CONDITION: str = """
Dexterity governs agility, reflexes, and balance. 
A Dexterity check applies to actions requiring quick, quiet, or precise movements, or maintaining stability on shaky ground.
Examples of Dexterity checks include:
Navigating a steep slope with a heavy cart
Making a sharp turn with a carriage
Picking a lock
Disarming a trap
Tying up a captive
Escaping restraints
Playing a stringed instrument
Crafting intricate or detailed items"""

    ATTACK_IMPACT: str = """
Attack and Damage Rolls
You add your Dexterity modifier to attack and damage rolls when using ranged weapons, such as a sling or longbow.
You also add your Dexterity modifier to attack and damage rolls when using melee weapons with the "Finesse" property, such as a dagger or rapier.
At the start of combat, you roll for initiative using a Dexterity check.
Initiative determines the turn order of creatures in the battle.
"""

    ARMOR_CLASS: str = (
        """Depending on the armor you wear, you can add your Dexterity modifier, or part of it, to your Armor Class."""
    )

    def get_when_characteristic_can_be_used(self) -> str:
        return Dexterity.USE_CONDITION

    def get_when_skill_can_be_used(self, skill: SkillType) -> str:
        if skill == SkillType.ACROBATICS:
            return SKILL_CONDITIONS[skill]
        elif skill == SkillType.SLEIGHT_OF_HAND:
            return SKILL_CONDITIONS[skill]
        elif skill == SkillType.STEALTH:
            return SKILL_CONDITIONS[skill]
        else:
            None

    def get_fight_impact(self):
        return Dexterity.ATTACK_IMPACT

    def get_social_impact(self) -> str:
        return None

    def get_exploration_impact(self) -> str:
        return None

    def get_stats_impact(self) -> str:
        return Dexterity.ARMOR_CLASS


class Constitution(Characteristic):
    name: Literal[CharacteristicType.CONSTITUTION] = CharacteristicType.CONSTITUTION
    skill_proficiencies: list[SkillType] = []
    USE_CONDITION: str = """
    Constitution checks are rare and no skills depend on it, as endurance is passive.
    However, a Constitution check might be called for when you:
    • Hold your breath
    • March or work for hours without rest
    • Go without sleep
    • Lack food and water
    • Attempt to drink a tankard of ale in one go
    """
    HITS_IMPACT: str = """
    Your Constitution modifier contributes to your hit points.
    You add your Constitution modifier to each Hit Die rolled for hit points. 
    If your Constitution modifier changes, your maximum hit points change as if the new modifier had been in place since level 1.
    """

    def get_when_characteristic_can_be_used(self) -> str:
        return self.USE_CONDITION

    def get_when_skill_can_be_used(self, skill: SkillType) -> str:
        return None

    def get_fight_impact(self) -> str:
        return self.HITS_IMPACT

    def get_social_impact(self) -> str:
        return None

    def get_exploration_impact(self) -> str:
        return None

    def get_stats_impact(self) -> str:
        return self.HITS_IMPACT


class Intelligence(Characteristic):
    name: Literal[CharacteristicType.INTELLIGENCE] = CharacteristicType.INTELLIGENCE
    skill_proficiencies: list[SkillType] = [
        SkillType.ARCANA,
        SkillType.HISTORY,
        SkillType.INVESTIGATION,
        SkillType.NATURE,
        SkillType.RELIGION,
    ]
    USE_CONDITION: str = """
    Intelligence measures mental acuity, accuracy of recall, and the ability to reason.
    Intelligence checks occur when you use logic, education, memory, or deductive reasoning.
    Skills like Arcana, History, Investigation, Nature, and Religion reflect a particular aptitude for certain Intelligence checks.
    Other Intelligence checks might be called for when you:
    • Communicate with a creature without using words
    • Appraise the value of a precious item
    • Disguise yourself as a city guard
    • Forge a document
    • Recall knowledge about a craft or trade
    • Compete with someone else
    """

    FIGHT_CONDITION: str = """
    Wizards use Intelligence to determine the save DCs of the spells they cast.
    """

    def get_when_characteristic_can_be_used(self) -> str:
        return self.USE_CONDITION

    def get_when_skill_can_be_used(self, skill: SkillType) -> str:
        if skill == SkillType.INVESTIGATION:
            return SKILL_CONDITIONS[skill]
        elif skill == SkillType.HISTORY:
            return SKILL_CONDITIONS[skill]
        elif skill == SkillType.ARCANA:
            return SKILL_CONDITIONS[skill]
        elif skill == SkillType.NATURE:
            return SKILL_CONDITIONS[skill]
        elif skill == SkillType.RELIGION:
            return SKILL_CONDITIONS[skill]
        else:
            return None

    def get_fight_impact(self) -> str:
        return self.FIGHT_CONDITION

    def get_social_impact(self) -> str:
        return None

    def get_exploration_impact(self) -> str:
        return self.USE_CONDITION

    def get_stats_impact(self) -> str:
        return None


class Wisdom(Characteristic):
    name: Literal[CharacteristicType.WISDOM] = CharacteristicType.WISDOM
    skill_proficiencies: list[SkillType] = [
        SkillType.ANIMAL_HANDLING,
        SkillType.INSIGHT,
        SkillType.MEDICINE,
        SkillType.PERCEPTION,
        SkillType.SURVIVAL,
    ]
    USE_CONDITION: str = """
    Wisdom reflects your awareness of your surroundings and intuition.
    Wisdom checks are called for when you rely on your senses, intuition, or perception.
    Skills like Animal Handling, Insight, Medicine, Perception, and Survival reflect a particular aptitude for certain Wisdom checks.
    Other Wisdom checks might be called for when you:
    • Sense a hidden motive
    • Detect a hidden object
    • Discern the true nature of a creature
    • Perceive the presence of magic
    • Resist being deceived
    • Predict the weather
    """

    SOCIAL_CONDITION: str = """
    A Wisdom check might be called for in social interactions when you need to sense the true intentions of others, detect lies, or understand the emotions of those around you.
    """

    EXPLORATION_CONDITION: str = """
    A Wisdom check might be called for during exploration when you need to find a hidden object, discover an ambush, or notice subtle changes in your environment that indicate danger.
    """

    def get_when_characteristic_can_be_used(self) -> str:
        return self.USE_CONDITION

    def get_when_skill_can_be_used(self, skill: SkillType) -> str:
        if skill == SkillType.ANIMAL_HANDLING:
            return SKILL_CONDITIONS[skill]
        elif skill == SkillType.INSIGHT:
            return SKILL_CONDITIONS[skill]
        elif skill == SkillType.MEDICINE:
            return SKILL_CONDITIONS[skill]
        elif skill == SkillType.PERCEPTION:
            return SKILL_CONDITIONS[skill]
        elif skill == SkillType.SURVIVAL:
            return SKILL_CONDITIONS[skill]
        else:
            return None

    def get_fight_impact(self) -> str:
        return None

    def get_social_impact(self) -> str:
        return self.SOCIAL_CONDITION

    def get_exploration_impact(self) -> str:
        return self.EXPLORATION_CONDITION

    def get_stats_impact(self) -> str:
        return None


class Charisma(Characteristic):
    name: Literal[CharacteristicType.CHARISMA] = CharacteristicType.CHARISMA
    skill_proficiencies: list[SkillType] = [
        SkillType.DECEPTION,
        SkillType.INTIMIDATION,
        SkillType.PERFORMANCE,
        SkillType.PERSUASION,
    ]
    USE_CONDITION: str = """
    Charisma measures your ability to interact effectively with others.
    Charisma checks are called for when you use your force of personality, charm, or leadership.
    Skills like Deception, Intimidation, Performance, and Persuasion reflect a particular aptitude for certain Charisma checks.
    Other Charisma checks might be called for when you:
    • Influence others with your presence
    • Make a good impression
    • Give a stirring speech
    • Convince others to agree with your point of view
    • Negotiate a deal
    • Settle a dispute
    """

    FIGHT_CONDITION: str = """
    Bards, sorcerers, paladins, and warlocks use Charisma to determine the save DCs of the spells they cast.
    """

    SOCIAL_CONDITION: str = """
    A Charisma check might be called for during social interactions when you need to influence, persuade, or deceive others, or when you want to make a strong impression in a conversation.
    """

    def get_when_characteristic_can_be_used(self) -> str:
        return self.USE_CONDITION

    def get_when_skill_can_be_used(self, skill: SkillType) -> str:
        return SKILL_CONDITIONS[skill]

    def get_fight_impact(self) -> str:
        return self.FIGHT_CONDITION

    def get_social_impact(self) -> str:
        return self.SOCIAL_CONDITION

    def get_exploration_impact(self) -> str:
        return None

    def get_stats_impact(self) -> str:
        return None
