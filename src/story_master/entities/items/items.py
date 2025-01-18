from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float | None = None
    weight: float = 0
    base_quantity: float = 1

class ItemStack(BaseModel):
    item: Item
    quantity: float

