from pydantic import BaseModel

from story_master.entities.items import Item


class Inventory(BaseModel):
    items: dict[str, Item] = dict()
    money: float = 0

    def add_item(self, item: Item):
        if item.name in self.items:
            self.items[item.name].quantity += item.quantity
        else:
            self.items[item.name] = item

    def remove_item(self, item_name: str, quantity: float):
        if item_name in self.items:
            self.items[item_name].quantity -= quantity
            if self.items[item_name].quantity <= 0:
                del self.items[item_name]

    def get_item(self, item_name: str) -> Item:
        return self.items[item_name]
