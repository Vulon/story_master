from story_master.memory.character import Character, CharacterNode
from story_master.memory.location import Location, LocationNode
from story_master.memory.faction import Faction, FactionNode
from story_master.memory.dialogue import Dialogue, DialogueNode
from story_master.memory.item import Item, ItemNode
from story_master.memory.entity import Entity
from story_master.memory.relation import (
    PartOfScene,
    LocatedNear,
    Carries,
    Wearing,
    Action,
    Talked,
    PartOfFaction,
    Social,
    Relation,
)


ENTITY_REGISTRY: dict[str, type[Entity]] = {
    Character.__name__: Character,
    Location.__name__: Location,
    Faction.__name__: Faction,
    Dialogue.__name__: Dialogue,
    Item.__name__: Item,
}

NODE_REGISTRY = {
    Character: CharacterNode,
    Location: LocationNode,
    Faction: FactionNode,
    Dialogue: DialogueNode,
    Item: ItemNode,
}

REVERSE_NODE_REGISTRY = {
    CharacterNode: Character,
    LocationNode: Location,
    FactionNode: Faction,
    DialogueNode: Dialogue,
    ItemNode: Item,
}

RELATION_REGISTRY: dict[str, type[Relation]] = {
    PartOfScene.__name__: PartOfScene,
    LocatedNear.__name__: LocatedNear,
    Carries.__name__: Carries,
    Wearing.__name__: Wearing,
    Action.__name__: Action,
    Talked.__name__: Talked,
    PartOfFaction.__name__: PartOfFaction,
    Social.__name__: Social,
}
