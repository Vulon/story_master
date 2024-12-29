from enum import StrEnum
from story_master.entities.items.items import Item


class InstrumentType(StrEnum):
    THIEVES_TOOLS = "Thieves' Tools"
    DRAGONCHESS_SET = "Dragonchess Set"
    PLAYING_CARDS = "Playing Cards"
    DICE_SET = "Dice Set"
    THREE_DRAGON_ANTE = "Three-Dragon Ante"
    NAVIGATORS_TOOLS = "Navigator's Tools"
    POISONERS_TOOLS = "Poisoner's Tools"
    ALCHEMISTS_SUPPLIES = "Alchemist's Supplies"
    POTTERS_TOOLS = "Potter's Tools"
    TINKERS_TOOLS = "Tinker's Tools"
    CALLIGRAPHERS_SUPPLIES = "Calligrapher's Supplies"
    MASONS_TOOLS = "Mason's Tools"
    CARTOGRAPHERS_TOOLS = "Cartographer's Tools"
    LEATHERWORKERS_TOOLS = "Leatherworker's Tools"
    SMITHS_TOOLS = "Smith's Tools"
    BREWERS_TOOLS = "Brewer's Tools"
    CARPENTERS_TOOLS = "Carpenter's Tools"
    COOKS_UTENSILS = "Cook's Utensils"
    WOODCARVERS_TOOLS = "Woodcarver's Tools"
    COBBLERS_TOOLS = "Cobbler's Tools"
    GLASSBLOWERS_TOOLS = "Glassblower's Tools"
    WEAVERS_TOOLS = "Weaver's Tools"
    PAINTERS_SUPPLIES = "Painter's Supplies"
    JEWELERS_TOOLS = "Jeweler's Tools"
    DRUM = "Drum"
    VIOL = "Viol"
    BAGPIPE = "Bagpipe"
    LYRE = "Lyre"
    LUTE = "Lute"
    HORN = "Horn"
    PAN_FLUTE = "Pan Flute"
    FLUTE = "Flute"
    CYMBALS = "Cymbals"
    SHAWM = "Shawm"
    DISGUISE_KIT = "Disguise Kit"
    FORGERY_KIT = "Forgery Kit"
    HERBALISM_KIT = "Herbalism Kit"


class Instrument(Item):
    description: str

    def get_full_description(self) -> str:
        return f"<Instrument>{self.name}: {self.description}. price={self.price}. weight={self.weight}</Instrument>"


INSTRUMENTS = {
    InstrumentType.THIEVES_TOOLS: Instrument(
        name=InstrumentType.THIEVES_TOOLS,
        price=25,
        weight=1,
        description="""
This set of tools includes a small file, a set of lock picks, a small mirror mounted on a metal handle,
a pair of scissors, and a pair of pliers. Proficiency with these tools lets you add your proficiency bonus
to any ability checks you make to disarm traps or open locks.
""",
    ),
    InstrumentType.DRAGONCHESS_SET: Instrument(
        name=InstrumentType.DRAGONCHESS_SET,
        price=1,
        weight=0.5,
        description="Dragonchess Set",
    ),
    InstrumentType.PLAYING_CARDS: Instrument(
        name=InstrumentType.PLAYING_CARDS,
        price=0.5,
        weight=0,
        description="Playing Cards",
    ),
    InstrumentType.DICE_SET: Instrument(
        name=InstrumentType.DICE_SET, price=0.1, weight=0, description="Dice Set"
    ),
    InstrumentType.THREE_DRAGON_ANTE: Instrument(
        name=InstrumentType.THREE_DRAGON_ANTE,
        price=1,
        weight=0,
        description="Three-Dragon Ante",
    ),
    InstrumentType.NAVIGATORS_TOOLS: Instrument(
        name=InstrumentType.NAVIGATORS_TOOLS,
        price=25,
        weight=2,
        description="""
These tools are used for navigation at sea. Proficiency with navigator's tools allows you to chart a ship's course 
and use sea charts. Additionally, these tools allow you to add your proficiency bonus to ability checks made 
to avoid getting lost at sea.
""",
    ),
    InstrumentType.POISONERS_TOOLS: Instrument(
        name=InstrumentType.POISONERS_TOOLS,
        price=50,
        weight=2,
        description="""
A poisoner's kit includes vials, chemicals, and other equipment needed to create poisons.
Proficiency in this set allows you to add your proficiency bonus to ability checks made create and use poisons.""",
    ),
    InstrumentType.ALCHEMISTS_SUPPLIES: Instrument(
        name=InstrumentType.ALCHEMISTS_SUPPLIES,
        price=50,
        weight=8,
        description="Alchemist's Supplies",
    ),
    InstrumentType.POTTERS_TOOLS: Instrument(
        name=InstrumentType.POTTERS_TOOLS,
        price=10,
        weight=3,
        description="Potter's Tools",
    ),
    InstrumentType.TINKERS_TOOLS: Instrument(
        name=InstrumentType.TINKERS_TOOLS,
        price=50,
        weight=10,
        description="Tinker's Tools",
    ),
    InstrumentType.CALLIGRAPHERS_SUPPLIES: Instrument(
        name=InstrumentType.CALLIGRAPHERS_SUPPLIES,
        price=10,
        weight=5,
        description="Calligrapher's Supplies",
    ),
    InstrumentType.MASONS_TOOLS: Instrument(
        name=InstrumentType.MASONS_TOOLS,
        price=10,
        weight=8,
        description="Mason's Tools",
    ),
    InstrumentType.CARTOGRAPHERS_TOOLS: Instrument(
        name=InstrumentType.CARTOGRAPHERS_TOOLS,
        price=15,
        weight=6,
        description="Cartographer's Tools",
    ),
    InstrumentType.LEATHERWORKERS_TOOLS: Instrument(
        name=InstrumentType.LEATHERWORKERS_TOOLS,
        price=5,
        weight=5,
        description="Leatherworker's Tools",
    ),
    InstrumentType.SMITHS_TOOLS: Instrument(
        name=InstrumentType.SMITHS_TOOLS,
        price=20,
        weight=8,
        description="Smith's Tools",
    ),
    InstrumentType.BREWERS_TOOLS: Instrument(
        name=InstrumentType.BREWERS_TOOLS,
        price=20,
        weight=9,
        description="Brewer's Tools",
    ),
    InstrumentType.CARPENTERS_TOOLS: Instrument(
        name=InstrumentType.CARPENTERS_TOOLS,
        price=8,
        weight=6,
        description="Carpenter's Tools",
    ),
    InstrumentType.COOKS_UTENSILS: Instrument(
        name=InstrumentType.COOKS_UTENSILS,
        price=1,
        weight=8,
        description="Cook's Utensils",
    ),
    InstrumentType.WOODCARVERS_TOOLS: Instrument(
        name=InstrumentType.WOODCARVERS_TOOLS,
        price=1,
        weight=5,
        description="Woodcarver's Tools",
    ),
    InstrumentType.COBBLERS_TOOLS: Instrument(
        name=InstrumentType.COBBLERS_TOOLS,
        price=5,
        weight=5,
        description="Cobbler's Tools",
    ),
    InstrumentType.GLASSBLOWERS_TOOLS: Instrument(
        name=InstrumentType.GLASSBLOWERS_TOOLS,
        price=30,
        weight=5,
        description="Glassblower's Tools",
    ),
    InstrumentType.WEAVERS_TOOLS: Instrument(
        name=InstrumentType.WEAVERS_TOOLS,
        price=1,
        weight=5,
        description="Weaver's Tools",
    ),
    InstrumentType.PAINTERS_SUPPLIES: Instrument(
        name=InstrumentType.PAINTERS_SUPPLIES,
        price=10,
        weight=5,
        description="Painter's Supplies",
    ),
    InstrumentType.JEWELERS_TOOLS: Instrument(
        name=InstrumentType.JEWELERS_TOOLS,
        price=25,
        weight=2,
        description="Jeweler's Tools",
    ),
    InstrumentType.DRUM: Instrument(
        name=InstrumentType.DRUM,
        price=6,
        weight=3,
        description="Drum",
    ),
    InstrumentType.VIOL: Instrument(
        name=InstrumentType.VIOL,
        price=30,
        weight=1,
        description="Viol",
    ),
    InstrumentType.BAGPIPE: Instrument(
        name=InstrumentType.BAGPIPE,
        price=30,
        weight=6,
        description="Bagpipe",
    ),
    InstrumentType.LYRE: Instrument(
        name=InstrumentType.LYRE,
        price=30,
        weight=2,
        description="Lyre",
    ),
    InstrumentType.LUTE: Instrument(
        name=InstrumentType.LUTE,
        price=35,
        weight=2,
        description="Lute",
    ),
    InstrumentType.HORN: Instrument(
        name=InstrumentType.HORN,
        price=3,
        weight=2,
        description="Horn",
    ),
    InstrumentType.PAN_FLUTE: Instrument(
        name=InstrumentType.PAN_FLUTE,
        price=12,
        weight=2,
        description="Pan Flute",
    ),
    InstrumentType.FLUTE: Instrument(
        name=InstrumentType.FLUTE,
        price=2,
        weight=1,
        description="Flute",
    ),
    InstrumentType.CYMBALS: Instrument(
        name=InstrumentType.CYMBALS,
        price=25,
        weight=10,
        description="Cymbals",
    ),
    InstrumentType.SHAWM: Instrument(
        name=InstrumentType.SHAWM,
        price=2,
        weight=1,
        description="Shawm",
    ),
    InstrumentType.DISGUISE_KIT: Instrument(
        name=InstrumentType.DISGUISE_KIT,
        price=25,
        weight=3,
        description="Disguise Kit",
    ),
    InstrumentType.FORGERY_KIT: Instrument(
        name=InstrumentType.FORGERY_KIT,
        price=15,
        weight=5,
        description="Forgery Kit",
    ),
    InstrumentType.HERBALISM_KIT: Instrument(
        name=InstrumentType.HERBALISM_KIT,
        price=5,
        weight=3,
        description="Herbalism Kit",
    ),
}


ARTISANS_TOOLS = [
    INSTRUMENTS[InstrumentType.ALCHEMISTS_SUPPLIES],
    INSTRUMENTS[InstrumentType.BREWERS_TOOLS],
    INSTRUMENTS[InstrumentType.CALLIGRAPHERS_SUPPLIES],
    INSTRUMENTS[InstrumentType.CARPENTERS_TOOLS],
    INSTRUMENTS[InstrumentType.CARTOGRAPHERS_TOOLS],
    INSTRUMENTS[InstrumentType.COBBLERS_TOOLS],
    INSTRUMENTS[InstrumentType.COOKS_UTENSILS],
    INSTRUMENTS[InstrumentType.GLASSBLOWERS_TOOLS],
    INSTRUMENTS[InstrumentType.JEWELERS_TOOLS],
    INSTRUMENTS[InstrumentType.LEATHERWORKERS_TOOLS],
    INSTRUMENTS[InstrumentType.MASONS_TOOLS],
    INSTRUMENTS[InstrumentType.PAINTERS_SUPPLIES],
    INSTRUMENTS[InstrumentType.POTTERS_TOOLS],
    INSTRUMENTS[InstrumentType.SMITHS_TOOLS],
    INSTRUMENTS[InstrumentType.TINKERS_TOOLS],
    INSTRUMENTS[InstrumentType.WEAVERS_TOOLS],
    INSTRUMENTS[InstrumentType.WOODCARVERS_TOOLS],
]
