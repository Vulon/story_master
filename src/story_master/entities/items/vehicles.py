from enum import StrEnum

from story_master.entities.items import Item


class TransportAnimalType(StrEnum):
    WARHORSE = "Warhorse"
    CAMEL = "Camel"
    RIDING_HORSE = "Riding Horse"
    DRAFT_HORSE = "Draft Horse"
    MASTIFF = "Mastiff"
    DONKEY_OR_MULE = "Donkey or Mule"
    PONY = "Pony"
    ELEPHANT = "Elephant"


class TransportUtilityType(StrEnum):
    CARRIAGE = "Carriage"
    CART = "Cart"
    SLED = "Sled"
    SADDLEBAGS = "Saddlebags"
    MILITARY_SADDLE = "Military Saddle"
    PACK_SADDLE = "Pack Saddle"
    RIDING_SADDLE = "Riding Saddle"
    EXOTIC_SADDLE = "Exotic Saddle"
    WAGON = "Wagon"
    HARNESS_AND_BIT = "Harness and Bit"
    WAGON = "Wagon"


class WaterTransportType(StrEnum):
    WARSHIP = "Warship"
    GALLEY = "Galley"
    KEELBOAT = "Keelboat"
    LONGSHIP = "Longship"
    SAILING_SHIP = "Sailing Ship"
    ROWBOAT = "Rowboat"


class Transport(Item):
    name: TransportAnimalType
    speed: int
    capacity: int


TRANSPORTS = {
    TransportAnimalType.WARHORSE: Transport(
        name=TransportAnimalType.WARHORSE,
        price=400,
        speed=60,
        capacity=540,
    ),
    TransportAnimalType.CAMEL: Transport(
        name=TransportAnimalType.CAMEL,
        price=50,
        speed=50,
        capacity=480,
    ),
    TransportAnimalType.RIDING_HORSE: Transport(
        name=TransportAnimalType.RIDING_HORSE,
        price=75,
        speed=60,
        capacity=480,
    ),
    TransportAnimalType.DRAFT_HORSE: Transport(
        name=TransportAnimalType.DRAFT_HORSE,
        price=50,
        speed=40,
        capacity=540,
    ),
    TransportAnimalType.MASTIFF: Transport(
        name=TransportAnimalType.MASTIFF,
        price=25,
        speed=40,
        capacity=195,
    ),
    TransportAnimalType.DONKEY_OR_MULE: Transport(
        name=TransportAnimalType.DONKEY_OR_MULE,
        price=8,
        speed=40,
        capacity=420,
    ),
    TransportAnimalType.PONY: Transport(
        name=TransportAnimalType.PONY,
        price=30,
        speed=40,
        capacity=225,
    ),
    TransportAnimalType.ELEPHANT: Transport(
        name=TransportAnimalType.ELEPHANT,
        price=200,
        speed=40,
        capacity=1320,
    ),
    WaterTransportType.WARSHIP: Transport(
        name=WaterTransportType.WARSHIP,
        price=25000,
        speed=2.5,
        capacity=0,  # Add appropriate capacity if needed
    ),
    WaterTransportType.GALLEY: Transport(
        name=WaterTransportType.GALLEY,
        price=30000,
        speed=4,
        capacity=0,  # Add appropriate capacity if needed
    ),
    WaterTransportType.KEELBOAT: Transport(
        name=WaterTransportType.KEELBOAT,
        price=3000,
        speed=1,
        capacity=0,  # Add appropriate capacity if needed
    ),
    WaterTransportType.LONGSHIP: Transport(
        name=WaterTransportType.LONGSHIP,
        price=10000,
        speed=3,
        capacity=0,  # Add appropriate capacity if needed
    ),
    WaterTransportType.SAILING_SHIP: Transport(
        name=WaterTransportType.SAILING_SHIP,
        price=10000,
        speed=2,
        capacity=0,  # Add appropriate capacity if needed
    ),
    WaterTransportType.ROWBOAT: Transport(
        name=WaterTransportType.ROWBOAT,
        price=50,
        speed=1.5,
        capacity=0,  # Add appropriate capacity if needed
    ),
}


TRANSPORT_UTILITIES = {
    TransportUtilityType.CARRIAGE: Item(
        name=TransportUtilityType.CARRIAGE,
        price=250,
        weight=100,
    ),
    TransportUtilityType.CART: Item(
        name=TransportUtilityType.CART,
        price=15,
        weight=200,
    ),
    TransportUtilityType.SLED: Item(
        name=TransportUtilityType.SLED,
        price=20,
        weight=300,
    ),
    TransportUtilityType.SADDLEBAGS: Item(
        name=TransportUtilityType.SADDLEBAGS,
        price=4,
        weight=8,
    ),
    TransportUtilityType.MILITARY_SADDLE: Item(
        name=TransportUtilityType.MILITARY_SADDLE,
        price=20,
        weight=30,
    ),
    TransportUtilityType.PACK_SADDLE: Item(
        name=TransportUtilityType.PACK_SADDLE,
        price=5,
        weight=15,
    ),
    TransportUtilityType.RIDING_SADDLE: Item(
        name=TransportUtilityType.RIDING_SADDLE,
        price=10,
        weight=25,
    ),
    TransportUtilityType.EXOTIC_SADDLE: Item(
        name=TransportUtilityType.EXOTIC_SADDLE,
        price=60,
        weight=40,
    ),
    TransportUtilityType.WAGON: Item(
        name=TransportUtilityType.WAGON,
        price=35,
        weight=400,
    ),
    TransportUtilityType.HARNESS_AND_BIT: Item(
        name=TransportUtilityType.HARNESS_AND_BIT,
        price=2,
        weight=1,
    ),
}
