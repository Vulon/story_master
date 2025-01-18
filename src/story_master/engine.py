from datetime import timedelta

from story_master.graphs.character_generation.character_generator import (
    CharacterGenerator,
)
from story_master.llm_client import get_client, get_embeddings_client
from story_master.phases.exploration import ExplorationManager
from story_master.phases.game_start import GameInitializer
from story_master.settings import Settings
from story_master.storage.storage_manager import StorageManager, CharacterStorage
from story_master.storage.storage_models import CharacterAction, ResourceGatheredEvent


class Engine:

    def __init__(self):
        self.settings = Settings()
        self.client = get_client()
        embeddings_client = get_embeddings_client()
        self.character_generator = CharacterGenerator(self.client)
        self.storage_manager = StorageManager(self.settings, embeddings_client)
        self.game_initializer = GameInitializer(
            self.storage_manager, self.client, self.settings
        )
        self.exploration_manager = ExplorationManager(
            self.storage_manager, self.client, self.settings
        )

    def run(self):
        self.game_initializer.initialize_game()

        main_player = self.storage_manager.character_storage.player_characters[self.settings.main_player_id]
        sim_queue = self.storage_manager.get_location_characters(
            self.storage_manager.get_location(main_player.current_location_id)
        )
        events_queue = self.storage_manager.game_storage.events_queue
        while True:
            if len(events_queue) == 0:
                print("Action queue is empty")
                player_action = CharacterAction(
                    sim_id=main_player.id, intent=input("Enter next action "),
                    timestamp=self.storage_manager.game_storage.current_time + timedelta(minutes=1)
                )
                events_queue.append(player_action)
            events_queue = sorted(events_queue, key=lambda x: x.timestamp)
            event = events_queue.pop(0)

            if isinstance(event, CharacterAction):
                self.exploration_manager.process_character_action(event)
            elif isinstance(event, ResourceGatheredEvent):
                self.exploration_manager.process_gathering_event(event)
