from story_master.graphs.character_generation.character_generator import (
    CharacterGenerator,
)
from story_master.llm_client import get_client, get_embeddings_client
from story_master.phases.exploration import ExplorationManager
from story_master.phases.game_start import GameInitializer
from story_master.settings import Settings
from story_master.storage.storage_manager import StorageManager


class Engine:

    def __init__(self):
        settings = Settings()
        self.client = get_client()
        embeddings_client = get_embeddings_client()
        self.character_generator = CharacterGenerator(self.client)
        self.storage_manager = StorageManager(settings, embeddings_client)
        self.game_initializer = GameInitializer(
            self.storage_manager, self.client, settings
        )
        self.exploration_manager = ExplorationManager(
            self.storage_manager, self.client, settings
        )

    def run(self):
        self.game_initializer.initialize_game()
        self.exploration_manager.run()
        # character_description = "A tall, strong, and wise old man. His axe helped him escape many dire situations."
        # generated_character = self.character_generator.generate(character_description)
