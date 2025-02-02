from story_master.llm_client import get_client, get_embeddings_client
from story_master.phases.game_start import GameInitializer
from story_master.settings import Settings
from story_master.storage.storage_manager import StorageManager
from story_master.storage.summary import SummaryAgent
from story_master.log import logger
from story_master.action_handling.action_handler import ActionHandler
from story_master.action_handling.actions.action_factory import ActionType


class Engine:
    def __init__(self):
        self.settings = Settings()
        self.client = get_client()
        embeddings_client = get_embeddings_client()
        self.storage_manager = StorageManager(self.settings, embeddings_client)
        self.summary_agent = SummaryAgent(self.storage_manager, self.client)

        self.action_handler = ActionHandler(
            self.client, self.summary_agent, self.storage_manager
        )

        self.game_initializer = GameInitializer(
            self.summary_agent, self.storage_manager, self.client, self.settings
        )

    def run(self):
        self.game_initializer.initialize_game()
        logger.info("Game initialized")
        main_player = self.storage_manager.character_storage.player_characters[
            self.settings.main_player_id
        ]
        sim_queue = self.storage_manager.get_location_characters(
            self.storage_manager.get_location(main_player.current_location_id)
        )
        events_queue = self.storage_manager.game_storage.events_queue

        self.storage_manager.clear_memories()

        # TODO: Add interior generation for character actions

        # self.action_handler.handle(
        #     ActionType.CREATE_CHARACTER,
        #     "Create a commoner character, that lives here",
        #     character_id=main_player.id
        # )
        #
        # self.action_handler.handle(
        #     ActionType.DIALOG,
        #     "I want to talk to the old mountain dwarf commoner: 'Hello, I am Taklinn. I am new here. Can you tell me about this place?'",
        #     character_id=main_player.id,
        # )

        # self.action_handler.handle(
        #     ActionType.INVESTIGATE_OBJECT,
        #     "I want to investigate the bed",
        #     character_id=main_player.id,
        # )

        self.action_handler.handle(
            ActionType.HARVEST_RESOURCES,
            "I want to break the bed and get some wood",
            character_id=main_player.id,
        )
