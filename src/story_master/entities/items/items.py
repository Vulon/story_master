from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float | None = None
    weight: float = 0
