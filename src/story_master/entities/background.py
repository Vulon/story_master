from enum import StrEnum

from pydantic import BaseModel

from story_master.entities.characteristics import SkillType
from story_master.entities.items.equipment import EQUIPMENT, EquipmentType
from story_master.entities.items.instruments import (
    ARTISANS_TOOLS,
    INSTRUMENTS,
    Instrument,
    InstrumentType,
)
from story_master.entities.items.items import Item
from story_master.utils.selection import SomeOf


class BackgroundType(StrEnum):
    ACOLYTE = "Acolyte"
    CHARLATAN = "Charlatan"
    CRIMINAL = "Criminal"
    ENTERTAINER = "Entertainer"
    FOLK_HERO = "Folk Hero"
    GUILD_ARTISAN = "Guild Artisan"
    HERMIT = "Hermit"
    NOBLE = "Noble"
    OUTLANDER = "Outlander"
    SAGE = "Sage"
    SAILOR = "Sailor"
    SOLDIER = "Soldier"
    URCHIN = "Urchin"


class FeatureType(StrEnum):
    SHELTER_OF_THE_FAITHFUL = "Shelter of the Faithful"
    FALSE_IDENTITY = "False Identity"
    RUSTIC_HOSPITALITY = "Rustic Hospitality"


FEATURES = {
    FeatureType.SHELTER_OF_THE_FAITHFUL: """
    You and your companions can expect free healing and care at temples, shrines, and other established places of your faith.
    You must provide any material components needed for spells.
    Those who share your faith will support you (but only you) at a modest lifestyle.
    You might have ties to a specific temple dedicated to your chosen deity or pantheon and have a residence there.
    While near your temple, you can call upon the priests for assistance, provided it does not endanger them.
    """,
    FeatureType.FALSE_IDENTITY: """
    You have created a second identity that includes documentation, established acquaintances,
    and disguises that allow you to assume that persona.
    Additionally, you can forge documents including official papers and personal letters,
    as long as you have seen an example of the kind of document or the handwriting you are trying to copy.
    """,
    FeatureType.RUSTIC_HOSPITALITY: """
    Since you come from the ranks of the common folk, you fit in among them with ease.
    You can find a place to hide, rest, or recuperate among other commoners, unless you have shown yourself to be a danger to them.
    They will shield you from the law or anyone else searching for you, though they will not risk their lives for you.
    """,
}


class Background(BaseModel):
    name: BackgroundType
    description: str
    skills: list[SkillType]
    money: float
    equipment: list[Item]
    tool_proficiencies: list[Instrument]
    feature: FeatureType
    base_traits: list[str]
    base_ideals: list[str]
    base_bonds: list[str]
    base_flaws: list[str]

    selected_trait: list[str] | None = None
    selected_ideal: list[str] | None = None
    selected_bond: list[str] | None = None
    selected_flaw: list[str] | None = None

    def get_description(self) -> str:
        full_description = [
            f"Background: {self.name}",
            f"Description: {self.description}",
            f"Feature: {FEATURES[self.feature]}",
            f"Traits: {', '.join(self.selected_trait)}",
            f"Ideal: {self.selected_ideal}",
            f"Bond: {self.selected_bond}",
            f"Flaw: {self.selected_flaw}",
        ]
        return "\n".join(full_description)

    def get_items_to_select(self):
        return [
            (
                "selected_trait",
                "base_traits",
                2,
                "Personality traits might describe the things the character likes, his or her past accomplishments, things the character dislikes or fears, character's self-attitude or mannerisms, or the influence of his or her ability scores.",
            ),
            (
                "selected_ideal",
                "base_ideals",
                1,
                "Ideals are beliefs that the character holds dear. They are the things that the character is willing to fight for, and they are the things that the character is willing to die for.",
            ),
            (
                "selected_bond",
                "base_bonds",
                1,
                "Bonds are relationships that the character has with other people, places, or things. They are the things that the character cares about, and they are the things that the character is willing to protect.",
            ),
            (
                "selected_flaw",
                "base_flaws",
                1,
                "Flaws are the character's weaknesses. They are the things that the character is afraid of, and they are the things that the character is ashamed of.",
            ),
        ]


class Charlatan(Background):
    name: BackgroundType = BackgroundType.CHARLATAN
    description: str = """
You have always had a way with people.
You know what makes them tick, you can tease out their hearts' desires after a few minutes of conversation,
and with a few leading questions you can read them like they were children's books.
It's a useful talent, and one that you're perfectly willing to use for your advantage.
You know what people want and you deliver, or rather, you promise to deliver.
Common sense should steer people away from things that sound too good to be true, 
but common sense seems to be in short supply when you're around.
The bottle of pink-colored liquid will surely cure that unseemly rash,
this ointment—nothing more than a bit of fat with a sprinkle of silver dust—can restore youth and vigor,
and there's a bridge in the city that just happens to be for sale. These marvels sound implausible, but you make them sound like the real deal
    """
    skills: list[SkillType] = [SkillType.DECEPTION, SkillType.SLEIGHT_OF_HAND]
    tool_proficiencies: list[Instrument] = [
        INSTRUMENTS[InstrumentType.DISGUISE_KIT],
        INSTRUMENTS[InstrumentType.FORGERY_KIT],
    ]
    money: float = 15
    equipment: list[Item] = [
        EQUIPMENT[EquipmentType.FINE_CLOTHES],
        INSTRUMENTS[InstrumentType.DISGUISE_KIT],
        EQUIPMENT[EquipmentType.POUCH],
    ]
    scams: list[str] = [
        "I cheat at games of chance.",
        "I shave coins or forge documents.",
        "I insinuate myself into people's lives to prey on their weakness and secure their fortunes.",
        "I put on new identities like clothes.",
        "I run sleight-of-hand cons on street corners.",
        "I convince people that worthless junk is worth their hard-earned money.",
    ]
    selected_scam: list[str] | None = None
    feature: FeatureType = FeatureType.FALSE_IDENTITY
    base_traits: list[str] = [
        "I fall in and out of love easily, and am always pursuing someone.",
        "I have a joke for every occasion, especially occasions where humor is inappropriate.",
        "Flattery is my preferred trick for getting what I want",
        "I'm a born gambler who can't resist taking a risk for a potential payoff.",
        "I lie about almost everything, even when there's no good reason to.",
        "Sarcasm and insults are my weapons of choice.",
    ]
    base_ideals: list[str] = [
        "Independence. I am a free spirit—no one tells me what to do. (Chaotic)",
        "Fairness. I never target people who can't afford to lose a few coins. (Lawful)",
        "Charity. I distribute the money I acquire to the people who really need it. (Good)",
        "Creativity. I never run the same con twice. (Chaotic)",
        "Friendship. Material goods come and go. Bonds of friendship last forever. (Good)",
        "Aspiration. I'm determined to make something of myself. (Any)",
    ]
    base_bonds: list[str] = [
        "I fleeced the wrong person and must work to ensure that this individual never crosses paths with me or those I care about.",
        "I owe everything to my mentor—a horrible person who's probably rotting in jail somewhere.",
        "Somewhere out there, I have a child who doesn't know me. I'm making the world better for him or her.",
        "I come from a noble family, and one day I'll reclaim my lands and title from those who stole them from me.",
        "A powerful person killed someone I love. Some day soon, I’ll have my revenge",
    ]
    base_flaws: list[str] = [
        "I can't resist a pretty face.",
        "I'm always in debt. I spend my ill-gotten gains on decadent luxuries faster than I bring them in.",
        "I'm convinced that no one could ever fool me the way I fool others.",
        "I'm too greedy for my own good. I can't resist taking a risk if there's money involved.",
        "I can't resist swindling people who are more powerful than me.",
        "I hate to admit it and will hate myself for it, but I'll run and preserve my own hide if the going gets tough.",
    ]

    def get_items_to_select(self):
        return super().get_items_to_select() + [
            (
                "selected_scam",
                "scams",
                1,
                "Scams are the ways the character uses to deceive people.",
            ),
        ]

    def get_description(self) -> str:
        return super().get_description() + f"\n Scam: {self.selected_scam}"


class FolkHero(Background):
    # Page 123
    name: BackgroundType = BackgroundType.FOLK_HERO
    description: str = """
    You come from a humble social rank, but you are destined for so much more.
    Already the people of your home village regard you as their champion, and your destiny calls you to stand against the tyrants and monsters that threaten the common folk everywhere
    """
    skills: list[SkillType] = [SkillType.ANIMAL_HANDLING, SkillType.SURVIVAL]
    tool_proficiencies: SomeOf = SomeOf(count=1, items=ARTISANS_TOOLS)
    equipment: list[Item | SomeOf] = [
        SomeOf(count=1, items=ARTISANS_TOOLS),
        EQUIPMENT[EquipmentType.SHOVEL],
        EQUIPMENT[EquipmentType.IRON_POT],
        EQUIPMENT[EquipmentType.COMMON_CLOTHES],
        EQUIPMENT[EquipmentType.POUCH],
    ]
    money: float = 10
    defining_events: list[str] = [
        "I stood up to a tyrant's agents.",
        "I saved people during a natural disaster.",
        "I stood alone against a terrible monster.",
        "I stole from a corrupt merchant to help the poor.",
        "I led a militia to fight off an invading army.",
        "I broke into a tyrant's castle and stole weapons to arm the people.",
        "I trained the peasantry to use farm implements as weapons against a tyrant's soldiers",
        "A lord rescinded an unpopular decree after I led a symbolic act of protect against it",
        "A celestial, fey, or similar creature gave me a blessing or revealed my secret origin.",
        "Recruited into a lord's army, I rose to leadership and was commended for my heroism.",
    ]
    selected_defining_event: list[str] | None = None

    def get_items_to_select(self):
        return super().get_items_to_select() + [
            (
                "selected_defining_event",
                "defining_events",
                1,
                "Defining events are the events that shaped the character's life and made him or her a hero.",
            ),
        ]

    def get_description(self) -> str:
        return (
            super().get_description()
            + f"\n Defining event: {self.selected_defining_event}"
        )

    feature: FeatureType = FeatureType.RUSTIC_HOSPITALITY
    base_traits: list[str] = [
        "I judge people by their actions, not their words.",
        "If someone is in trouble, I'm always ready to lend help.",
        "When I set my mind to something, I follow through no matter what gets in my way.",
        "I have a strong sense of fair play and always try to find the most equitable solution to arguments.",
        "I'm confident in my own abilities and do what I can to instill confidence in others.",
        "Thinking is for other people. I prefer action.",
        "I misuse long words in an attempt to sound smarter.",
        "I get bored easily. When am I going to get on with my destiny?",
    ]
    base_ideals: list[str] = [
        "Respect. People deserve to be treated with dignity and respect. (Good)",
        "Fairness. No one should get preferential treatment before the law, and no one is above the law. (Lawful)",
        "Freedom. Tyrants must not be allowed to oppress the people. (Chaotic)",
        "Might. If I become strong, I can take what I want—what I deserve. (Evil)",
        "Sincerity. There's no good in pretending to be something I'm not. (Neutral)",
        "Destiny. Nothing and no one can steer me away from my higher calling. (Any)",
    ]
    base_bonds: list[str] = [
        "I have a family, but I have no idea where they are. One day, I hope to see them again.",
        "I worked the land, I love the land, and I will protect the land.",
        "A proud noble once gave me a horrible beating, and I will take my revenge on any bully I encounter.",
        "My tools are symbols of my past life, and I carry them so that I will never forget my roots.",
        "I protect those who cannot protect themselves.",
        "I wish my childhood sweetheart had come with me to pursue my destiny.",
    ]
    base_flaws: list[str] = [
        "The tyrant who rules my land will stop at nothing to see me killed.",
        "I'm convinced of the significance of my destiny, and blind to my shortcomings and the risk of failure.",
        "The people who knew me when I was young know my shameful secret, so I can never go home again.",
        "I have a weakness for the vices of the city, especially hard drink.",
        "Secretly, I believe that things would be better if I were a tyrant lording over the land.",
        "I have trouble trusting in my allies.",
    ]


BACKGROUNDS: dict[BackgroundType, Background] = {
    BackgroundType.ACOLYTE: Background(
        name=BackgroundType.ACOLYTE,
        description="""
You have spent your life in the service of a temple to a specific god or pantheon of gods. 
You act as an intermediary between the realm of the holy and the mortal world, performing sacred rites and offering sacrifices in order to conduct worshipers into the presence of the divine. 
You are not necessarily a cleric-perform ing sacred rites is not the same thing as channeling divine power
        """,
        skills=[SkillType.INSIGHT, SkillType.RELIGION],
        money=15,
        equipment=[
            EQUIPMENT[EquipmentType.HOLY_SYMBOL_AMULET],
            EQUIPMENT[EquipmentType.PRAYER_BOOK],
            EQUIPMENT[EquipmentType.RELIGIOUS_CLOTHES],
            EQUIPMENT[EquipmentType.COMMON_CLOTHES],
            EQUIPMENT[EquipmentType.POUCH],
        ]
        + [EQUIPMENT[EquipmentType.INCENSE]] * 5,
        feature=FeatureType.SHELTER_OF_THE_FAITHFUL,
        tool_proficiencies=[],
        base_traits=[
            "I idolize a particular hero of my faith, and constantly refer to that person's deeds and example.",
            "I can find common ground between the fiercest enemies, empathizing with them and always working towards peace.",
            "I see omens in every event and action. The gods try to speak to us, we just need to listen.",
            "Nothing can shake my optimistic attitude.",
            "I quote (or misquote) sacred texts and proverbs in almost every situation.",
            "I am tolerant (or intolerant) of other faiths and respect (or condemn) the worship of other gods.",
            "I've spent so long in the temple that I have little practical experience dealing with people in the outside world.",
        ],
        base_ideals=[
            "Tradition. The ancient traditions of worship and sacrifice must be preserved and upheld. (Lawful)",
            "Charity. I always try to help those in need, no matter what the personal cost. (Good)",
            "Change. We must help bring about the changes the gods are constantly working in the world. (Chaotic)",
            "Power. I hope to one day rise to the top of my faith's religious hierarchy. (Lawful)",
            "Faith. I trust that my deity will guide my actions. I have faith that if I work hard, things will go well. (Lawful)",
            "Aspiration. I seek to prove myself worthy of my god's favor by matching my actions against their teachings. (Any)",
        ],
        base_bonds=[
            "I would die to recover an ancient relic of my faith that was lost long ago.",
            "I will someday get revenge on the corrupt temple hierarchy who branded me a heretic.",
            "I owe my life to the priest who took me in when my parents died.",
            "Everything I do is for the common people.",
            "I will do anything to protect the temple where I served.",
            "I seek to preserve a sacred text that my enemies consider heretical and seek to destroy.",
        ],
        base_flaws=[
            "I judge others harshly, and myself even more severely.",
            "I put too much trust in those who wield power within my temple's hierarchy.",
            "My piety sometimes leads me to blindly trust those that profess faith in my god.",
            "I am inflexible in my thinking.",
            "I am suspicious of strangers and expect the worst of them.",
            "Once I pick a goal, I become obsessed with it to the detriment of everything else in my life.",
        ],
    ),
    BackgroundType.CHARLATAN: Charlatan(),
    BackgroundType.FOLK_HERO: FolkHero(),
}


# Page 128
