from pydantic import BaseModel
from story_master.entities.handlers.storage_handler import StorageHandler


class get_nearby_characters(BaseModel):
    """
    Retrieval function.
    Gets a list of all characters nearby.
    Each character is described by their appearance.
    """


ANY_TOOL = get_nearby_characters


class WorldRetriever:
    def __init__(self, storage_handler: StorageHandler):
        self.storage_handler = storage_handler

    def get_nearby_characters(self, sim_id: int, radius: int = 3) -> str:
        main_sim = self.storage_handler.get_sim(sim_id)
        position = main_sim.position
        close_sims = []
        for (
            other_sim_id,
            other_sim,
        ) in self.storage_handler.character_storage.npc_characters.items():
            if other_sim_id == sim_id:
                continue
            if position.is_close(other_sim.position, radius):
                close_sims.append(other_sim)

        sim_strings = [
            f"<Sim>ID: {sim.id}. Details: {sim.character.get_external_description()}</Sim>"
            for sim in close_sims
        ]

        return ", ".join(sim_strings)
