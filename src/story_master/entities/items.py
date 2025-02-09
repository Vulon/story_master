from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str
    weight: float = 0
    quantity: float

