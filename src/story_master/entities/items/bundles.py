from story_master.entities.items.equipment import EQUIPMENT, EquipmentType
from story_master.entities.items.instruments import INSTRUMENTS, InstrumentType


ARTIST_BUNDLE = (
    [
        EQUIPMENT[EquipmentType.BAG],
        EQUIPMENT[EquipmentType.BEDROLL],
        EQUIPMENT[EquipmentType.COSTUME],
        EQUIPMENT[EquipmentType.COSTUME],
        EQUIPMENT[EquipmentType.WATERSKIN],
        INSTRUMENTS[InstrumentType.DISGUISE_KIT],
    ]
    + [EQUIPMENT[EquipmentType.CANDLE]] * 5
    + [EQUIPMENT[EquipmentType.RATIONS]] * 5
)

THIEF_BUNDLE = (
    [
        EQUIPMENT[EquipmentType.BAG],
        EQUIPMENT[EquipmentType.METAL_BALLS],
        EQUIPMENT[EquipmentType.BELL],
        EQUIPMENT[EquipmentType.LANTERN_HOODED],
        EQUIPMENT[EquipmentType.OIL_FLASK],
        EQUIPMENT[EquipmentType.OIL_FLASK],
        EQUIPMENT[EquipmentType.TINDERBOX],
        EQUIPMENT[EquipmentType.WATERSKIN],
        EQUIPMENT[EquipmentType.HEMP_ROPE],
    ]
    + [EQUIPMENT[EquipmentType.CANDLE]] * 5
    + [EQUIPMENT[EquipmentType.PITON]] * 10
    + [EQUIPMENT[EquipmentType.RATIONS]] * 5
)

DIPLOMAT_BUNDLE = [
    EQUIPMENT[EquipmentType.CHEST],
    EQUIPMENT[EquipmentType.FINE_CLOTHES],
    EQUIPMENT[EquipmentType.INK],
    EQUIPMENT[EquipmentType.LAMP],
    EQUIPMENT[EquipmentType.OIL_FLASK],
    EQUIPMENT[EquipmentType.OIL_FLASK],
    EQUIPMENT[EquipmentType.PERFUME_VIAL],
    EQUIPMENT[EquipmentType.SOAP],
    EQUIPMENT[EquipmentType.WAX],
] + [EQUIPMENT[EquipmentType.PARCHMENT]] * 5

DUNGEONEER_BUNDLE = [
    EQUIPMENT[EquipmentType.BAG],
    EQUIPMENT[EquipmentType.CROWBAR],
    EQUIPMENT[EquipmentType.HAMMER],
    EQUIPMENT[EquipmentType.TINDERBOX],
    EQUIPMENT[EquipmentType.WATERSKIN],
    EQUIPMENT[EquipmentType.HEMP_ROPE],
] + [
    EQUIPMENT[EquipmentType.PITON],
    EQUIPMENT[EquipmentType.TORCH],
    EQUIPMENT[EquipmentType.RATIONS],
] * 10

EXPLORER_BUNDLE = [
    EQUIPMENT[EquipmentType.BAG],
    EQUIPMENT[EquipmentType.BEDROLL],
    EQUIPMENT[EquipmentType.MESS_KIT],
    EQUIPMENT[EquipmentType.TINDERBOX],
    EQUIPMENT[EquipmentType.WATERSKIN],
    EQUIPMENT[EquipmentType.HEMP_ROPE],
] + [EQUIPMENT[EquipmentType.TORCH], EQUIPMENT[EquipmentType.RATIONS]] * 10

# TODO: Add more items to this bundle
CLERIC_BUNDLE = (
    [
        EQUIPMENT[EquipmentType.BAG],
        EQUIPMENT[EquipmentType.BLANKET],
        EQUIPMENT[EquipmentType.TINDERBOX],
        EQUIPMENT[EquipmentType.WATERSKIN],
        EQUIPMENT[EquipmentType.COMMON_CLOTHES],
        EQUIPMENT[EquipmentType.RELIGIOUS_CLOTHES],
    ]
    + [EQUIPMENT[EquipmentType.CANDLE]] * 10
    + [EQUIPMENT[EquipmentType.RATIONS]] * 2
    + [EQUIPMENT[EquipmentType.INCENSE]] * 5
)

# TODO: Add knife and sand bag
SCIENCIST_BUNDLE = [
    EQUIPMENT[EquipmentType.BAG],
    EQUIPMENT[EquipmentType.BOOK],
    EQUIPMENT[EquipmentType.INK],
    EQUIPMENT[EquipmentType.BAG],
] + [EQUIPMENT[EquipmentType.PARCHMENT]] * 10
