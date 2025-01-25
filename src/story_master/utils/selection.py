from typing import Iterable

from pydantic import BaseModel


class SomeOf(BaseModel):
    count: int
    items: list


def get_batched(items: Iterable, batch_size: int):
    items = list(items)
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]
