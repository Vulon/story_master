from enum import StrEnum

from story_master.entities.items.items import Item


class Equipment(Item):
    length: int | None = None
    description: str = ""


class EquipmentType(StrEnum):
    ABACUS = "Abacus"
    ALCHEMISTS_FIRE = "Alchemist's Fire (flask)"
    BLOCK_AND_TACKLE = "Block and Tackle"
    CROSSBOW_BOLTS = "Crossbow Bolts"
    BLOWGUN_NEEDLES = "Blowgun Needles"
    SLING_BULLETS = "Sling Bullets"
    ARROWS = "Arrows"
    BARREL = "Barrel"
    PAPER = "Paper"
    WATERSKIN = "Waterskin"
    GLASS_BOTTLE = "Glass Bottle"
    BUCKET = "Bucket"
    HEMP_ROPE = "Hemp Rope"
    SILK_ROPE = "Silk Rope"
    MERCHANTS_SCALE = "Merchant's Scale"
    WAX = "Wax"
    IRON_POT = "Iron Pot"
    PERFUME_VIAL = "Perfume (vial)"
    LOCK = "Lock"
    HEALING_POTION = "Healing Potion"
    STEEL_MIRROR = "Steel Mirror"
    CALTROPS = "Caltrops"
    MANACLES = "Manacles"
    MINERS_PICK = "Miner's Pick"
    ACID_VIAL = "Acid (vial)"
    BOOK = "Book"
    SPELLBOOK = "Spellbook"
    PRAYER_BOOK = "Prayer Book"
    BELL = "Bell"
    QUIVER = "Quiver"
    SIGNET_RING = "Signet Ring"
    CLIMBERS_KIT = "Climber's Kit"
    FISHING_TACKLE = "Fishing Tackle"
    HEALERS_KIT = "Healer's Kit"
    CROSSBOW_BOLT_CASE = "Crossbow Bolt Case"
    MAP_OR_SCROLL_CASE = "Map or Scroll Case"
    BASKET = "Basket"
    POUCH = "Pouch"
    GRAPPLING_HOOK = "Grappling Hook"
    JUG_OR_PITCHER = "Jug or Pitcher"
    LAMP = "Lamp"
    LADDER = "Ladder"
    CROWBAR = "Crowbar"
    SHOVEL = "Shovel"
    MAGIC_FOCUS = "Magic Focus"
    WAND = "Wand"
    ROD = "Rod"
    CRYSTAL = "Crystal"
    STAFF = "Staff"
    ORB = "Orb"
    OIL_FLASK = "Oil (flask)"
    CHALK = "Chalk"
    METAL_BALLS = "Metal Balls"
    BAG = "Bag"
    COMPONENT_POUCH = "Component Pouch"
    SMITHS_HAMMER = "Smith's Hammer"
    HAMMER = "Hammer"
    SOAP = "Soap"
    TRAVELERS_CLOTHES = "Traveler's Clothes"
    COSTUME = "Costume"
    COMMON_CLOTHES = "Common Clothes"
    FINE_CLOTHES = "Fine Clothes"
    RELIGIOUS_CLOTHES = "Religious Clothes"
    BLANKET = "Blanket"
    HUNTING_TRAP = "Hunting Trap"
    TENT = "Tent"
    PARCHMENT = "Parchment"
    HOURGLASS = "Hourglass"
    QUILL = "Quill"
    SPYGLASS = "Spyglass"
    ANTITOXIN = "Antitoxin"
    RATIONS = "Rations"
    BACKPACK = "Backpack"
    ROBES = "Robes"
    CANDLE = "Candle"
    HOLY_WATER = "Holy Water"
    HOLY_SYMBOL_AMULET = "Holy Symbol Amulet"
    HOLY_SYMBOL_RELIQUARY = "Holy Symbol Reliquary"
    HOLY_SYMBOL_EMBLEM = "Holy Symbol Emblem"
    SIGNAL_WHISTLE = "Signal Whistle"
    BEDROLL = "Bedroll"
    MESS_KIT = "Mess Kit"
    CHEST = "Chest"
    RAM = "Portable Ram"
    WHETSTONE = "Whetstone"
    TINDERBOX = "Tinderbox"
    MAGNIFYING_GLASS = "Magnifying Glass"
    TORCH = "Torch"
    VIAL = "Vial"
    FLASK_OR_TANKARD = "Flask or Tankard"
    DRUIDIC_FOCUS_MISTLETOE = "Druidic Focus Mistletoe"
    DRUIDIC_FOCUS_WOODEN_STAFF = "Druidic Focus Wooden Staff"
    DRUIDIC_FOCUS_YEW_WAND = "Druidic Focus Yew Wand"
    DRUIDIC_FOCUS_TOTEM = "Druidic Focus Totem"
    LANTERN_BULLSEYE = "Bullseye Lantern"
    LANTERN_HOODED = "Hooded Lantern"
    CHAIN = "Chain"
    INK = "Ink"
    POLE = "Pole"
    IRON_SPIKES = "Iron Spikes"
    PITON = "Piton"
    BASIC_POISON = "Basic Poison"
    INCENSE = "Incense"


EQUIPMENT = {
    EquipmentType.ABACUS: Equipment(
        name="Abacus",
        price=2,
        weight=2,
    ),
    EquipmentType.ALCHEMISTS_FIRE: Equipment(
        name="Alchemist's Fire (flask)",
        price=50,
        weight=1,
    ),
    EquipmentType.BLOCK_AND_TACKLE: Equipment(
        name="Block and Tackle",
        price=1,
        weight=5,
    ),
    EquipmentType.CROSSBOW_BOLTS: Equipment(
        name="Crossbow Bolts",
        price=1,
        weight=1.5,
        base_quantity=20,
    ),
    EquipmentType.BLOWGUN_NEEDLES: Equipment(
        name="Blowgun Needles",
        price=1,
        weight=1,
        base_quantity=50,
    ),
    EquipmentType.SLING_BULLETS: Equipment(
        name="Sling Bullets",
        price=0.04,
        weight=1.5,
        base_quantity=20,
    ),
    EquipmentType.ARROWS: Equipment(
        name="Arrows",
        price=1,
        weight=1,
        base_quantity=20,
    ),
    EquipmentType.BARREL: Equipment(
        name="Barrel",
        price=2,
        weight=70,
    ),
    EquipmentType.PAPER: Equipment(
        name="Paper",
        price=0.2,
    ),
    EquipmentType.WATERSKIN: Equipment(
        name="Waterskin",
        price=0.2,
        weight=5,
    ),
    EquipmentType.GLASS_BOTTLE: Equipment(
        name="Glass Bottle",
        price=2,
        weight=2,
    ),
    EquipmentType.BUCKET: Equipment(
        name="Bucket",
        price=0.05,
        weight=2,
    ),
    EquipmentType.HEMP_ROPE: Equipment(
        name="Hemp Rope",
        price=1,
        weight=10,
        length=50,
        description="Hemp rope has 2 hit points and can be burst with a DC 17 Strength check.",
    ),
    EquipmentType.SILK_ROPE: Equipment(
        name="Silk Rope",
        price=10,
        weight=5,
        length=50,
        description="Silk rope has 2 hit points and can be burst with a DC 17 Strength check.",
    ),
    EquipmentType.MERCHANTS_SCALE: Equipment(
        name="Merchant's Scale",
        price=5,
        weight=3,
        description="A scale includes a small balance, pans, and a suitable assortment of weights up to 2 pounds.",
    ),
    EquipmentType.WAX: Equipment(
        name="Wax",
        price=0.5,
    ),
    EquipmentType.IRON_POT: Equipment(
        name="Iron Pot",
        price=2,
        weight=10,
    ),
    EquipmentType.PERFUME_VIAL: Equipment(
        name="Perfume (vial)",
        price=5,
    ),
    EquipmentType.LOCK: Equipment(
        name="Lock",
        price=10,
        weight=1,
        description="A key is provided with the lock. Without the key, a creature proficient with thieves' tools can pick this lock with a successful DC 15 Dexterity check.",
    ),
    EquipmentType.HEALING_POTION: Equipment(
        name="Healing Potion",
        price=50,
        weight=0.5,
        description="A character who drinks the magical red fluid in this vial regains 2d4 + 2 hit points. Drinking or administering a potion takes an action.",
    ),
    EquipmentType.STEEL_MIRROR: Equipment(
        name="Steel Mirror",
        price=5,
        weight=0.5,
    ),
    EquipmentType.CALTROPS: Equipment(
        name="Caltrops",
        price=1,
        weight=2,
        base_quantity=20,
        description="As an action, you can spread a bag of caltrops to cover a square area that is 5 feet on a side. Any creature that enters the area must succeed on a DC 15 Dexterity saving throw or stop moving and take 1 piercing damage. Until the creature regains at least 1 hit point, its walking speed is reduced by 10 feet. A creature moving through the area at half speed doesn't need to make the saving throw.",
    ),
    EquipmentType.MANACLES: Equipment(
        name="Manacles",
        price=2,
        weight=6,
        description="These metal restraints can bind a Small or Medium creature. Escaping the manacles requires a successful DC 20 Dexterity check. Breaking them requires a successful DC 20 Strength. Each set of manacles comes with one key. Without the key, a creature proficient with thieves' tools can pick the manacles' lock with a successful DC 15 Dexterity check.",
    ),
    EquipmentType.MINERS_PICK: Equipment(
        name="Miner's Pick",
        price=2,
        weight=10,
    ),
    EquipmentType.ACID_VIAL: Equipment(
        name="Acid (vial)",
        price=25,
        weight=1,
    ),
    EquipmentType.BOOK: Equipment(
        name="Book",
        price=25,
        weight=5,
    ),
    EquipmentType.SPELLBOOK: Equipment(
        name="Spellbook",
        price=50,
        weight=3,
    ),
    EquipmentType.PRAYER_BOOK: Equipment(
        name=EquipmentType.PRAYER_BOOK,
        price=None,
        weight=3,
    ),
    EquipmentType.BELL: Equipment(
        name="Bell",
        price=1,
    ),
    EquipmentType.QUIVER: Equipment(
        name="Quiver",
        price=1,
        weight=1,
    ),
    EquipmentType.SIGNET_RING: Equipment(
        name="Signet Ring",
        price=5,
    ),
    EquipmentType.CLIMBERS_KIT: Equipment(
        name="Climber's Kit",
        price=25,
        weight=12,
    ),
    EquipmentType.FISHING_TACKLE: Equipment(
        name="Fishing Tackle",
        price=1,
        weight=4,
    ),
    EquipmentType.HEALERS_KIT: Equipment(
        name="Healer's Kit",
        price=5,
        weight=3,
    ),
    EquipmentType.CROSSBOW_BOLT_CASE: Equipment(
        name="Crossbow Bolt Case",
        price=1,
        weight=1,
    ),
    EquipmentType.MAP_OR_SCROLL_CASE: Equipment(
        name="Map or Scroll Case",
        price=1,
        weight=1,
    ),
    EquipmentType.BASKET: Equipment(
        name="Basket",
        price=0.4,
        weight=2,
    ),
    EquipmentType.POUCH: Equipment(
        name="Pouch",
        price=0.5,
        weight=1,
    ),
    EquipmentType.GRAPPLING_HOOK: Equipment(
        name="Grappling Hook",
        price=2,
        weight=4,
    ),
    EquipmentType.JUG_OR_PITCHER: Equipment(
        name="Jug or Pitcher",
        price=0.02,
        weight=4,
    ),
    EquipmentType.LAMP: Equipment(
        name="Lamp",
        price=0.5,
        weight=1,
    ),
    EquipmentType.LADDER: Equipment(
        name="Ladder",
        price=0.1,
        weight=25,
    ),
    EquipmentType.CROWBAR: Equipment(
        name="Crowbar",
        price=2,
        weight=5,
    ),
    EquipmentType.SHOVEL: Equipment(
        name="Shovel",
        price=2,
        weight=5,
    ),
    EquipmentType.MAGIC_FOCUS: Equipment(
        name="Magic Focus",
        price=10,
        weight=1,
    ),
    EquipmentType.WAND: Equipment(
        name="Wand",
        price=10,
        weight=1,
    ),
    EquipmentType.ROD: Equipment(
        name="Rod",
        price=10,
        weight=2,
    ),
    EquipmentType.CRYSTAL: Equipment(
        name="Crystal",
        price=10,
        weight=1,
    ),
    EquipmentType.STAFF: Equipment(
        name="Staff",
        price=5,
        weight=4,
    ),
    EquipmentType.ORB: Equipment(
        name="Orb",
        price=20,
        weight=3,
    ),
    EquipmentType.OIL_FLASK: Equipment(
        name="Oil (flask)",
        price=0.1,
        weight=1,
    ),
    EquipmentType.CHALK: Equipment(
        name="Chalk",
        price=0.01,
    ),
    EquipmentType.METAL_BALLS: Equipment(
        name="Metal Balls",
        price=1,
        weight=2,
        base_quantity=1000,
    ),
    EquipmentType.BAG: Equipment(
        name="Bag",
        price=0.01,
        weight=0.5,
    ),
    EquipmentType.COMPONENT_POUCH: Equipment(
        name="Component Pouch",
        price=25,
        weight=2,
    ),
    EquipmentType.SMITHS_HAMMER: Equipment(
        name="Smith's Hammer",
        price=2,
        weight=10,
    ),
    EquipmentType.HAMMER: Equipment(
        name="Hammer",
        price=1,
        weight=3,
    ),
    EquipmentType.SOAP: Equipment(
        name="Soap",
        price=0.02,
    ),
    EquipmentType.TRAVELERS_CLOTHES: Equipment(
        name="Traveler's Clothes",
        price=2,
        weight=4,
    ),
    EquipmentType.COSTUME: Equipment(
        name="Costume",
        price=5,
        weight=4,
    ),
    EquipmentType.RELIGIOUS_CLOTHES: Equipment(
        name=EquipmentType.RELIGIOUS_CLOTHES,
        price=0.5,
        weight=3,
    ),
    EquipmentType.COMMON_CLOTHES: Equipment(
        name="Common Clothes",
        price=0.5,
        weight=3,
    ),
    EquipmentType.FINE_CLOTHES: Equipment(
        name="Fine Clothes",
        price=15,
        weight=6,
    ),
    EquipmentType.BLANKET: Equipment(
        name="Blanket",
        price=0.5,
        weight=3,
    ),
    EquipmentType.HUNTING_TRAP: Equipment(
        name="Hunting Trap",
        price=5,
        weight=25,
    ),
    EquipmentType.TENT: Equipment(
        name="Tent",
        price=2,
        weight=20,
    ),
    EquipmentType.PARCHMENT: Equipment(
        name="Parchment",
        price=0.1,
    ),
    EquipmentType.HOURGLASS: Equipment(
        name="Hourglass",
        price=25,
        weight=1,
    ),
    EquipmentType.QUILL: Equipment(
        name="Quill",
        price=0.02,
    ),
    EquipmentType.SPYGLASS: Equipment(
        name="Spyglass",
        price=1000,
        weight=1,
    ),
    EquipmentType.ANTITOXIN: Equipment(
        name="Antitoxin",
        price=50,
    ),
    EquipmentType.RATIONS: Equipment(
        name="Rations",
        price=0.5,
        weight=2,
    ),
    EquipmentType.BACKPACK: Equipment(
        name="Backpack",
        price=2,
        weight=5,
    ),
    EquipmentType.ROBES: Equipment(
        name="Robes",
        price=1,
        weight=4,
    ),
    EquipmentType.CANDLE: Equipment(
        name="Candle",
        price=0.01,
    ),
    EquipmentType.HOLY_WATER: Equipment(
        name="Holy Water",
        price=25,
        weight=1,
    ),
    EquipmentType.HOLY_SYMBOL_AMULET: Equipment(
        name="Holy Symbol Amulet",
        price=5,
        weight=1,
    ),
    EquipmentType.HOLY_SYMBOL_RELIQUARY: Equipment(
        name="Holy Symbol Reliquary",
        price=5,
        weight=2,
    ),
    EquipmentType.HOLY_SYMBOL_EMBLEM: Equipment(
        name="Holy Symbol Emblem",
        price=5,
    ),
    EquipmentType.SIGNAL_WHISTLE: Equipment(
        name="Signal Whistle",
        price=0.05,
    ),
    EquipmentType.BEDROLL: Equipment(
        name="Bedroll",
        price=1,
        weight=7,
    ),
    EquipmentType.MESS_KIT: Equipment(
        name="Mess Kit",
        price=0.2,
        weight=1,
    ),
    EquipmentType.CHEST: Equipment(
        name="Chest",
        price=5,
        weight=25,
    ),
    EquipmentType.RAM: Equipment(
        name="Portable Ram",
        price=4,
        weight=35,
    ),
    EquipmentType.WHETSTONE: Equipment(
        name="Whetstone",
        price=0.01,
        weight=1,
    ),
    EquipmentType.TINDERBOX: Equipment(
        name="Tinderbox",
        price=0.5,
        weight=1,
    ),
    EquipmentType.MAGNIFYING_GLASS: Equipment(
        name="Magnifying Glass",
        price=100,
    ),
    EquipmentType.TORCH: Equipment(
        name="Torch",
        price=0.01,
        weight=1,
    ),
    EquipmentType.VIAL: Equipment(
        name="Vial",
        price=1,
    ),
    EquipmentType.FLASK_OR_TANKARD: Equipment(
        name="Flask or Tankard",
        price=0.02,
        weight=1,
    ),
    EquipmentType.DRUIDIC_FOCUS_MISTLETOE: Equipment(
        name="Druidic Focus Mistletoe",
        price=1,
    ),
    EquipmentType.DRUIDIC_FOCUS_WOODEN_STAFF: Equipment(
        name="Druidic Focus Wooden Staff",
        price=5,
        weight=4,
    ),
    EquipmentType.DRUIDIC_FOCUS_YEW_WAND: Equipment(
        name="Druidic Focus Yew Wand",
        price=10,
        weight=1,
    ),
    EquipmentType.DRUIDIC_FOCUS_TOTEM: Equipment(
        name="Druidic Focus Totem",
        price=1,
    ),
    EquipmentType.LANTERN_BULLSEYE: Equipment(
        name="Bullseye Lantern",
        price=10,
        weight=2,
    ),
    EquipmentType.LANTERN_HOODED: Equipment(
        name="Hooded Lantern",
        price=5,
        weight=2,
    ),
    EquipmentType.CHAIN: Equipment(
        name="Chain",
        price=5,
        weight=10,
        length=10,
    ),
    EquipmentType.INK: Equipment(
        name="Ink",
        price=10,
    ),
    EquipmentType.POLE: Equipment(
        name="Pole",
        price=0.05,
        weight=7,
        length=10,
    ),
    EquipmentType.IRON_SPIKES: Equipment(
        name="Iron Spikes",
        price=1,
        weight=5,
        base_quantity=10,
    ),
    EquipmentType.PITON: Equipment(
        name="Piton",
        price=0.05,
        weight=0.25,
    ),
    EquipmentType.BASIC_POISON: Equipment(
        name="Basic Poison",
        price=100,
    ),
    EquipmentType.INCENSE: Equipment(
        name=EquipmentType.INCENSE,
    ),
}
