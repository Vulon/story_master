from story_master.settings import Settings
from story_master.memory.entity import Entity, EntityNode
from story_master.db_client import get_db
from story_master.memory.registry import (
    NODE_REGISTRY,
)


class DatabaseManager:
    def __init__(self):
        self.db = get_db()
        self.settings = Settings()
        self.db.drop_database()

    def save_entity(self, entity: Entity) -> Entity:
        node_class = NODE_REGISTRY[type(entity)]
        kwargs = entity.to_dict()
        kwargs["session"] = self.settings.session
        node = node_class(**kwargs)
        return self.db.save_node(node)

    def load_entity(self, name: str) -> list:
        node = EntityNode(name=name, session=self.settings.session)
        return self.db.load_node(node)
