from story_master.memory.location import Location, LocationNode
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
    Location.__name__: Location,
}

NODE_REGISTRY = {
    Location: LocationNode,
}

REVERSE_NODE_REGISTRY = {
    LocationNode: Location,
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
