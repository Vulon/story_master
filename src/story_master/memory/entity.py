from gqlalchemy import Node, Field
from pydantic import BaseModel
from abc import abstractmethod
from story_master.db_client import get_db


db = get_db()


class EntityNode(Node, db=db):
    session: int = Field(unique=True, db=db)

    def to_dict(self) -> dict:
        pass


class Entity(BaseModel):
    session: int | None = None

    @classmethod
    def get_class_description(cls) -> str:
        pass

    @classmethod
    def get_fields_description(cls) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass
