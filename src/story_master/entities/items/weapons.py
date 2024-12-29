from enum import StrEnum
from story_master.entities.items.items import Item
from story_master.entities.characteristics import DamageType


class WeaponType(StrEnum):
    QUARTERSTAFF = "Quarterstaff"
    MACE = "Mace"
    CLUB = "Club"
    DAGGER = "Dagger"
    SPEAR = "Spear"
    LIGHT_HAMMER = "Light Hammer"
    JAVELIN = "Javelin"
    MAUL = "Maul"
    HANDAXE = "Handaxe"
    SICKLE = "Sickle"
    LIGHT_CROSSBOW = "Light Crossbow"
    DART = "Dart"
    SHORTBOW = "Shortbow"
    SLING = "Sling"
    # War weapons
    HALBERD = "Halberd"
    WAR_PICK = "War Pick"
    WARHAMMER = "Warhammer"
    BATTLEAXE = "Battleaxe"
    GLAIVE = "Glaive"
    GREATSWORD = "Greatsword"
    LANCE = "Lance"
    LONGSWORD = "Longsword"
    WHIP = "Whip"
    SHORTSWORD = "Shortsword"
    MORNINGSTAR = "Morningstar"
    PIKE = "Pike"
    RAPIER = "Rapier"
    GREATAXE = "Greataxe"
    SCIMITAR = "Scimitar"
    TRIDENT = "Trident"
    FLAIL = "Flail"
    HAND_CROSSBOW = "Hand Crossbow"
    HEAVY_CROSSBOW = "Heavy Crossbow"
    LONG_BOW = "Long Bow"
    BLOWGUN = "Blowgun"


SIMPLE_WEAPONS = [
    WeaponType.QUARTERSTAFF,
    WeaponType.MACE,
    WeaponType.CLUB,
    WeaponType.DAGGER,
    WeaponType.SPEAR,
    WeaponType.LIGHT_HAMMER,
    WeaponType.JAVELIN,
    WeaponType.MAUL,
    WeaponType.HANDAXE,
    WeaponType.SICKLE,
    WeaponType.LIGHT_CROSSBOW,
    WeaponType.DART,
    WeaponType.SHORTBOW,
    WeaponType.SLING,
]

WAR_WEAPONS = [
    WeaponType.HALBERD,
    WeaponType.WAR_PICK,
    WeaponType.WARHAMMER,
    WeaponType.BATTLEAXE,
    WeaponType.GLAIVE,
    WeaponType.GREATSWORD,
    WeaponType.LANCE,
    WeaponType.LONGSWORD,
    WeaponType.WHIP,
    WeaponType.SHORTSWORD,
    WeaponType.MORNINGSTAR,
    WeaponType.PIKE,
    WeaponType.RAPIER,
    WeaponType.GREATAXE,
    WeaponType.SCIMITAR,
    WeaponType.TRIDENT,
    WeaponType.FLAIL,
    WeaponType.HAND_CROSSBOW,
    WeaponType.HEAVY_CROSSBOW,
    WeaponType.LONG_BOW,
    WeaponType.BLOWGUN,
]


class Weapon(Item):
    damage_dice: int
    damage_type: DamageType
    ammunition: bool = False
    two_handed: bool = False
    long_reach: bool = False
    distance: int | None = None
    max_distance: int | None = None
    light: bool = False
    throwing: bool = False
    special_rule: str | None = None
    requires_reload: bool = False
    heavy: bool = False
    versatile_damage: int | None = None
    finesse: bool = False


WEAPONS = {
    WeaponType.QUARTERSTAFF: Weapon(
        name="Quarterstaff",
        price=0.2,
        weight=4,
        damage_dice=6,
        damage_type=DamageType.BLUDGEONING,
        versatile_damage=8,
    ),
    WeaponType.MACE: Weapon(
        name="Mace",
        price=5,
        weight=4,
        damage_dice=6,
        damage_type=DamageType.BLUDGEONING,
    ),
    WeaponType.CLUB: Weapon(
        name="Club",
        price=0.1,
        weight=2,
        damage_dice=4,
        damage_type=DamageType.BLUDGEONING,
        light=True,
    ),
    WeaponType.DAGGER: Weapon(
        name="Dagger",
        price=2,
        weight=1,
        damage_dice=4,
        damage_type=DamageType.PIERCING,
        distance=20,
        max_distance=60,
        light=True,
        throwing=True,
        finesse=True,
    ),
    WeaponType.SPEAR: Weapon(
        name="Spear",
        price=1,
        weight=3,
        damage_dice=6,
        damage_type=DamageType.PIERCING,
        distance=20,
        max_distance=60,
        throwing=True,
        versatile_damage=8,
    ),
    WeaponType.LIGHT_HAMMER: Weapon(
        name="Light Hammer",
        price=2,
        weight=2,
        damage_dice=4,
        damage_type=DamageType.BLUDGEONING,
        distance=20,
        max_distance=60,
        light=True,
        throwing=True,
    ),
    WeaponType.JAVELIN: Weapon(
        name="Javelin",
        price=0.5,
        weight=2,
        damage_dice=6,
        damage_type=DamageType.PIERCING,
        distance=30,
        max_distance=120,
        throwing=True,
    ),
    WeaponType.MAUL: Weapon(
        name="Maul",
        price=0.2,
        weight=10,
        damage_dice=8,
        damage_type=DamageType.BLUDGEONING,
        two_handed=True,
        heavy=True,
    ),
    WeaponType.HANDAXE: Weapon(
        name="Handaxe",
        price=5,
        weight=2,
        damage_dice=6,
        damage_type=DamageType.SLASHING,
        distance=20,
        max_distance=60,
        light=True,
        throwing=True,
    ),
    WeaponType.SICKLE: Weapon(
        name="Sickle",
        price=1,
        weight=2,
        damage_dice=4,
        damage_type=DamageType.SLASHING,
        light=True,
    ),
    WeaponType.LIGHT_CROSSBOW: Weapon(
        name="Light Crossbow",
        price=25,
        weight=5,
        damage_dice=8,
        damage_type=DamageType.PIERCING,
        distance=80,
        max_distance=320,
        two_handed=True,
        requires_reload=True,
        ammunition=True,
    ),
    WeaponType.DART: Weapon(
        name="Dart",
        price=0.05,
        weight=0.25,
        damage_dice=4,
        damage_type=DamageType.PIERCING,
        distance=20,
        max_distance=60,
        throwing=True,
        finesse=True,
    ),
    WeaponType.SHORTBOW: Weapon(
        name="Shortbow",
        price=25,
        weight=2,
        damage_dice=6,
        damage_type=DamageType.PIERCING,
        distance=80,
        max_distance=320,
        two_handed=True,
        ammunition=True,
    ),
    WeaponType.SLING: Weapon(
        name="Sling",
        price=0.1,
        weight=0,
        damage_dice=4,
        damage_type=DamageType.BLUDGEONING,
        distance=30,
        max_distance=120,
        ammunition=True,
    ),
    # War weapons
    WeaponType.HALBERD: Weapon(
        name="Halberd",
        price=20,
        weight=6,
        damage_dice=10,
        damage_type=DamageType.SLASHING,
        two_handed=True,
        long_reach=True,
        heavy=True,
    ),
    WeaponType.WAR_PICK: Weapon(
        name="War Pick",
        price=5,
        weight=2,
        damage_dice=8,
        damage_type=DamageType.PIERCING,
    ),
    WeaponType.WARHAMMER: Weapon(
        name="Warhammer",
        price=15,
        weight=2,
        damage_dice=8,
        damage_type=DamageType.BLUDGEONING,
        versatile_damage=10,
    ),
    WeaponType.BATTLEAXE: Weapon(
        name="Battleaxe",
        price=10,
        weight=4,
        damage_dice=8,
        damage_type=DamageType.SLASHING,
        versatile_damage=10,
    ),
    WeaponType.GLAIVE: Weapon(
        name="Glaive",
        price=20,
        weight=6,
        damage_dice=10,
        damage_type=DamageType.SLASHING,
        two_handed=True,
        long_reach=True,
        heavy=True,
    ),
    WeaponType.GREATSWORD: Weapon(
        name="Greatsword",
        price=50,
        weight=6,
        damage_dice=12,
        damage_type=DamageType.SLASHING,
        two_handed=True,
        heavy=True,
    ),
    WeaponType.LANCE: Weapon(
        name="Lance",
        price=10,
        weight=6,
        damage_dice=12,
        damage_type=DamageType.PIERCING,
        long_reach=True,
    ),
    WeaponType.LONGSWORD: Weapon(
        name="Longsword",
        price=15,
        weight=3,
        damage_dice=8,
        damage_type=DamageType.SLASHING,
        versatile_damage=10,
    ),
    WeaponType.WHIP: Weapon(
        name="Whip",
        price=2,
        weight=3,
        damage_dice=4,
        damage_type=DamageType.SLASHING,
        long_reach=True,
        finesse=True,
    ),
    WeaponType.SHORTSWORD: Weapon(
        name="Shortsword",
        price=10,
        weight=2,
        damage_dice=6,
        damage_type=DamageType.PIERCING,
        light=True,
        finesse=True,
    ),
    WeaponType.MAUL: Weapon(
        name="Maul",
        price=10,
        weight=10,
        damage_dice=12,
        damage_type=DamageType.BLUDGEONING,
        two_handed=True,
        heavy=True,
    ),
    WeaponType.MORNINGSTAR: Weapon(
        name="Morningstar",
        price=15,
        weight=4,
        damage_dice=8,
        damage_type=DamageType.PIERCING,
    ),
    WeaponType.PIKE: Weapon(
        name="Pike",
        price=5,
        weight=18,
        damage_dice=10,
        damage_type=DamageType.PIERCING,
        two_handed=True,
        long_reach=True,
        heavy=True,
    ),
    WeaponType.RAPIER: Weapon(
        name="Rapier",
        price=25,
        weight=2,
        damage_dice=8,
        damage_type=DamageType.PIERCING,
        finesse=True,
    ),
    WeaponType.GREATAXE: Weapon(
        name="Greataxe",
        price=30,
        weight=7,
        damage_dice=12,
        damage_type=DamageType.SLASHING,
        two_handed=True,
        heavy=True,
    ),
    WeaponType.SCIMITAR: Weapon(
        name="Scimitar",
        price=25,
        weight=3,
        damage_dice=6,
        damage_type=DamageType.SLASHING,
        light=True,
        finesse=True,
    ),
    WeaponType.TRIDENT: Weapon(
        name="Trident",
        price=5,
        weight=4,
        damage_dice=6,
        damage_type=DamageType.PIERCING,
        distance=20,
        max_distance=60,
        throwing=True,
        versatile_damage=8,
    ),
    WeaponType.FLAIL: Weapon(
        name="Flail",
        price=10,
        weight=2,
        damage_dice=8,
        damage_type=DamageType.BLUDGEONING,
    ),
    WeaponType.HAND_CROSSBOW: Weapon(
        name="Hand Crossbow",
        price=75,
        weight=3,
        damage_dice=6,
        damage_type=DamageType.PIERCING,
        distance=30,
        max_distance=120,
        light=True,
        requires_reload=True,
        ammunition=True,
    ),
    WeaponType.HEAVY_CROSSBOW: Weapon(
        name="Heavy Crossbow",
        price=50,
        weight=18,
        damage_dice=10,
        damage_type=DamageType.PIERCING,
        distance=100,
        max_distance=400,
        two_handed=True,
        requires_reload=True,
        heavy=True,
        ammunition=True,
    ),
    WeaponType.LONG_BOW: Weapon(
        name="Long Bow",
        price=50,
        weight=2,
        damage_dice=8,
        damage_type=DamageType.PIERCING,
        distance=150,
        max_distance=600,
        two_handed=True,
        heavy=True,
        ammunition=True,
    ),
    WeaponType.BLOWGUN: Weapon(
        name="Blowgun",
        price=10,
        weight=1,
        damage_dice=1,
        damage_type=DamageType.PIERCING,
        distance=25,
        max_distance=100,
        requires_reload=True,
        ammunition=True,
    ),
}
