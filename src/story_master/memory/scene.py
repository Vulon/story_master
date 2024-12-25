from story_master.memory.entity import Entity, EntityNode
from gqlalchemy import Field

CLASS_DESCRIPTION = """A scene. Represents a specific location or event in the story."""
CLASS_FIELDS_DESCRIPTION = """
class Scene.
Represents a specific location or event in the story.
Fields:
{{
 "name": "Name of the scene."
}}
"""


class Scene(Entity):
    name: str
    number: int

    @classmethod
    def get_class_description(cls) -> str:
        return CLASS_DESCRIPTION

    @classmethod
    def get_fields_description(cls):
        return CLASS_FIELDS_DESCRIPTION

    def to_dict(self) -> dict:
        return self.model_dump()


class SceneNode(EntityNode):
    name: str = Field(unique=True)
    number: int = Field(unique=True)

    def to_dict(self) -> dict:
        return self.model_dump()
