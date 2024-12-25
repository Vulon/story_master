from enum import StrEnum

from pydantic import BaseModel


class Service(BaseModel):
    name: str
    price: float
    description: str


class ServiceType(StrEnum):
    STABLE = "Stable"
    FODDER = "Fodder"
    COMMON_WINE_MUG = "Common Wine Mug"
    FINE_WINE_BOTTLE = "Fine Wine Bottle"
    PIECE_OF_MEAT = "Piece of Meat"
    BEER_GALLON = "Beer Gallon"
    BEAR_MUG = "Bear Mug"
    PIECE_OF_CHESSE = "Piece of Cheese"
    LOAF_OF_BREAD = "Loaf of Bread"
    FEAST = "Feast"
    NOVICE_MERCENARY = "Novice Mercenary"
    VETERAN_MERCENARY = "Veteran Mercenary"
    CARRIAGE_RIDE_WITHIN_CITY = "Carriage Ride Within City"
    CARRIAGE_RIDE_BETWEEN_CITIES = "Carriage Ride Between Cities"
    MESSENGER = "Messenger"
    ROAD_OR_GATE_TOLL = "Road or Gate Toll"
    SHIP_PASSAGE = "Ship Passage"


class LifeStyleType(StrEnum):
    WRETCHED = "Wretched"
    SQUALID = "Squalid"
    POOR = "Poor"
    MODEST = "Modest"
    COMFORTABLE = "Comfortable"
    WEALTHY = "Wealthy"
    ARISTOCRATIC = "Aristocratic"


class InnType(StrEnum):
    SQUALID = "Squalid"
    POOR = "Poor"
    MODEST = "Modest"
    COMFORTABLE = "Comfortable"
    WEALTHY = "Wealthy"
    ARISTOCRATIC = "Aristocratic"


# Types of food diet per day
class DietType(StrEnum):
    SQUALID = "Squalid"
    POOR = "Poor"
    MODEST = "Modest"
    COMFORTABLE = "Comfortable"
    WEALTHY = "Wealthy"
    ARISTOCRATIC = "Aristocratic"


LIFESTYLES = {
    LifeStyleType.WRETCHED: Service(
        name=LifeStyleType.WRETCHED,
        price=0,
        description="""
You live in inhumane conditions. 
You have no home, you sleep wherever you can, scavenging for scraps, hiding under crates,
and relying on handouts from those who are better off than you.
This wretched lifestyle is perilous. 
You are constantly plagued by violence, disease, and hunger. 
Those who share your miserable existence covet your armor, weapons, and equipment, as they are a fortune to them. You are always being watched.""",
    ),
    LifeStyleType.SQUALID: Service(
        name=LifeStyleType.SQUALID,
        price=0.1,
        description="""
You live in a leaky stall, a dugout outside the city, or a bug-infested shelter in the slums. You are sheltered from the elements, but the environment is still dangerous, as it threatens disease, hunger and failure. Many people are watching you, and the law hardly protects you. Many of those who lead such an existence experience difficulties. They are given no rest
they are labeled as outcasts and suffer from diseases.""",
    ),
    LifeStyleType.POOR: Service(
        name=LifeStyleType.POOR,
        price=0.2,
        description="""
A poor existence means a lack of goods available in a stable society.
Monotonous food and poor lodging, torn clothes and an unpredictable future lead to unpleasant consequences.
You can live in a room in a bunkhouse or in a common room above the tavern.
The law partially protects you, but you still have to deal with violence,crimes and diseases.
Those who lead such an existence usually work as laborers, hawkers, peddlers, thieves and occupy other low-prestige positions""",
    ),
    LifeStyleType.MODEST: Service(
        name=LifeStyleType.MODEST,
        price=1,
        description="""
Living modestly gets you out of the slums and means you can maintain your gear.
You live in the old part of the city, renting a room in a boarding house, inn or temple.
You are not tormented by hunger or thirst, and you live in purity, albeit in a simple way. 
Soldiers and their families, laborers, students, priests, novice wizards and others.""",
    ),
    LifeStyleType.COMFORTABLE: Service(
        name=LifeStyleType.COMFORTABLE,
        price=2,
        description="""
Living comfortably means you can afford good clothes and keep your equipment in good condition.
You live in a small house with middle-class neighbors or in a private room in a good inn.
You do business with merchants, experienced traders and military officers.""",
    ),
    LifeStyleType.WEALTHY: Service(
        name=LifeStyleType.WEALTHY,
        price=4,
        description="""
A wealthy existence means a life of luxury, although you may not have the inherited wealth of nobles or royalty.
Successful merchants, beloved servants at court, or owners of several successful businesses lead the same life as you.
You have a comfortable home, usually this is a spacious house in a good area of ​​the city or a comfortable room in an excellent hotel.
Perhaps you have several servants.""",
    ),
    LifeStyleType.ARISTOCRATIC: Service(
        name=LifeStyleType.ARISTOCRATIC,
        price=10,
        description="""
You live in abundance and comfort. You move among the most influential members of society.
You have an excellent home, perhaps a mansion in the best part of town or a few rooms in a great hotel.
You eat in the best restaurants, dress from fashionable tailors, and have servants for every occasion.
You receive invitations to gatherings of the rich and powerful, and in the evenings you gather in the company of politicians, guild heads, high priests and nobles. You are threatened by lies and betrayal. 
The richer you are, the greater the chance that you will be drawn into political intrigue.""",
    ),
}

INN_SERVICES = {
    InnType.SQUALID: Service(
        name=InnType.SQUALID,
        price=0.07,
    ),
    InnType.POOR: Service(
        name=InnType.POOR,
        price=0.1,
    ),
    InnType.MODEST: Service(
        name=InnType.MODEST,
        price=0.5,
    ),
    InnType.COMFORTABLE: Service(
        name=InnType.COMFORTABLE,
        price=0.8,
    ),
    InnType.WEALTHY: Service(
        name=InnType.WEALTHY,
        price=2,
    ),
    InnType.ARISTOCRATIC: Service(
        name=InnType.ARISTOCRATIC,
        price=4,
    ),
}

DIETS = {
    DietType.SQUALID: Service(
        name=DietType.SQUALID,
        price=0.03,
    ),
    DietType.POOR: Service(
        name=DietType.POOR,
        price=0.06,
    ),
    DietType.MODEST: Service(
        name=DietType.MODEST,
        price=0.3,
    ),
    DietType.COMFORTABLE: Service(
        name=DietType.COMFORTABLE,
        price=0.5,
    ),
    DietType.WEALTHY: Service(
        name=DietType.WEALTHY,
        price=0.8,
    ),
    DietType.ARISTOCRATIC: Service(
        name=DietType.ARISTOCRATIC,
        price=2,
    ),
}


SERVICES = {
    ServiceType.STABLE: Service(
        name=ServiceType.STABLE,
        price=0.5,
        description="A place to keep your horse safe and fed.",
    ),
    ServiceType.FODDER: Service(
        name="Fodder",
        price=0.05,
        description="A day's worth of food for your horse. (10 lbs)",
    ),
    ServiceType.COMMON_WINE_MUG: Service(
        name=ServiceType.COMMON_WINE_MUG,
        price=0.2,
        description="A mug of common wine.",
    ),
    ServiceType.FINE_WINE_BOTTLE: Service(
        name=ServiceType.FINE_WINE_BOTTLE,
        price=10,
        description="A bottle of fine wine.",
    ),
    ServiceType.PIECE_OF_MEAT: Service(
        name=ServiceType.PIECE_OF_MEAT,
        price=3,
        description="A piece of meat.",
    ),
    ServiceType.BEER_GALLON: Service(
        name=ServiceType.BEER_GALLON,
        price=0.2,
        description="A gallon of beer.",
    ),
    ServiceType.BEAR_MUG: Service(
        name=ServiceType.BEAR_MUG,
        price=0.04,
        description="A mug of bear.",
    ),
    ServiceType.PIECE_OF_CHESSE: Service(
        name=ServiceType.PIECE_OF_CHESSE,
        price=0.1,
        description="A piece of cheese.",
    ),
    ServiceType.LOAF_OF_BREAD: Service(
        name=ServiceType.LOAF_OF_BREAD,
        price=0.02,
        description="A loaf of bread.",
    ),
    ServiceType.FEAST: Service(
        name=ServiceType.FEAST,
        price=10,
        description="A feast for a single person.",
    ),
    ServiceType.CARRIAGE_RIDE_WITHIN_CITY: Service(
        name=ServiceType.CARRIAGE_RIDE_WITHIN_CITY,
        price=0.01,
        description="Carriage ride within the city.",
    ),
    ServiceType.CARRIAGE_RIDE_BETWEEN_CITIES: Service(
        name=ServiceType.CARRIAGE_RIDE_BETWEEN_CITIES,
        price=0.03,
        description="Carriage ride between cities per mile.",
    ),
    ServiceType.MESSENGER: Service(
        name=ServiceType.MESSENGER,
        price=0.02,
        description="Messenger service per mile.",
    ),
    ServiceType.ROAD_OR_GATE_TOLL: Service(
        name=ServiceType.ROAD_OR_GATE_TOLL,
        price=0.01,
        description="Road or gate toll.",
    ),
    ServiceType.SHIP_PASSAGE: Service(
        name=ServiceType.SHIP_PASSAGE,
        price=0.1,
        description="Ship passage per mile.",
    ),
}
