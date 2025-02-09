from pydantic import BaseModel
from story_master.entities.character import ANY_CHARACTER
from story_master.entities.location import Position
from story_master.entities.inventory import Inventory
from story_master.entities.memory import Memory

class Sim(BaseModel):
    id: int
    character: ANY_CHARACTER
    position: Position
    inventory: Inventory
    memory: Memory
    current_status: str = ""

