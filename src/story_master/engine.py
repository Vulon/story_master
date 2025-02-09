from story_master.llm_client import get_client, get_embeddings_client

from story_master.settings import Settings
from story_master.log import logger
from story_master.action_handling.action_handler import ActionHandler
from story_master.action_handling.actions.action_factory import ActionType
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.entities.handlers.observation_handler import ObservationHandler
from story_master.generators.environment_generation.map_creator import MapCreator

class Engine:
    def __init__(self):
        self.settings = Settings()
        self.client = get_client()
        embeddings_client = get_embeddings_client()

        self.storage_handler = StorageHandler(self.settings)
        self.summary_handler = SummaryHandler(self.client)
        self.memory_handler = MemoryHandler(self.client, embeddings_client, self.storage_handler)
        self.observation_handler = ObservationHandler(
            self.client, self.memory_handler,
        )

        self.action_handler = ActionHandler(
            self.client, self.summary_handler, self.storage_handler
        )

        self.map_creator = MapCreator(self.client, self.storage_handler, self.summary_handler)

    def run(self):
        self.storage_handler.map.locations = dict()

        self.map_creator.create_map()
