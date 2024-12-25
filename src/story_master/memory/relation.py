from gqlalchemy import Relationship
from abc import ABC, abstractmethod


class Relation(Relationship, ABC):
    @classmethod
    @abstractmethod
    def get_class_description(cls):
        pass


class PartOfScene(Relationship, type="PART_OF_SCENE"):

    @classmethod
    def get_class_description(cls):
        return "Shows that an entity is linked to a scene"


class LocatedNear(Relationship, type="LOCATED_NEAR"):
    distance: float | None = None

    @classmethod
    def get_class_description(cls):
        return "Shows that one location is accessible from another location"


class Carries(Relationship, type="CARRIES"):
    @classmethod
    def get_class_description(cls):
        return "Shows that a character has an item"


class Wearing(Relationship, type="WEARING"):
    @classmethod
    def get_class_description(cls):
        return "Shows that the character wears an item"


class Action(Relationship, type="ACTION"):
    action_type: str

    @classmethod
    def get_class_description(cls):
        return "Shows that one character performed an action on another character"


class Talked(Relationship, type="TALKED"):
    @classmethod
    def get_class_description(cls):
        return "Links the dialogue to characters"


class PartOfFaction(Relationship, type="PART_OF_FACTION"):
    @classmethod
    def get_class_description(cls):
        return "Shows that a character is a part of the faction"


class Social(Relationship, type="SOCIAL"):
    relationship_type: str

    @classmethod
    def get_class_description(cls):
        return "Shows the social relationship between characters"
