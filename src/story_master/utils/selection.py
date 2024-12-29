from pydantic import BaseModel


class SomeOf(BaseModel):
    count: int
    items: list
