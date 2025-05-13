from story_master.entities.handlers.event_handler import EventHandler
from story_master.llm_client import get_client, get_embeddings_client

from story_master.settings import Settings
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.generators.environment_generation.map_creator import MapCreator


class Engine:
    def __init__(self):
        self.settings = Settings()
        self.client = get_client()
        embeddings_client = get_embeddings_client()

        self.storage_handler = StorageHandler(self.settings)
        self.summary_handler = SummaryHandler(self.client)
        self.memory_handler = MemoryHandler(
            embeddings_client, self.settings.storage, self.storage_handler
        )
        self.event_handler = EventHandler(self.storage_handler)

        self.map_creator = MapCreator(
            self.client, self.storage_handler, self.summary_handler
        )

    def run(self):
        # self.storage_handler.map.locations = dict()
        #
        # self.map_creator.create_map()
        # center = Position(location_id=0, x=0, y=0)
        # self.map_creator.generate_area(center, 7)
        # self.storage_handler.save_map()

        # self.action_handler.handle_system_action(ActionType.SPAWN_SIM)
        # self.action_handler.handle_system_action(ActionType.SPAWN_SIM)
        # self.storage_handler.save_characters()

        # for i in range(2):
        #     logger.info(f"Itteration {i}")
        #     for sim_id in self.storage_handler.character_storage.npc_characters.keys():
        #         logger.info(f"Processing sim {sim_id}")
        #         self.sim_ai_handler.handle(sim_id)
        #         print("\n" * 5)
        pass
