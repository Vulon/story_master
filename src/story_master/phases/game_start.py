import random

from langchain_core.language_models.chat_models import BaseChatModel

from story_master.generators.character_generation.character_generator import (
    CharacterGenerator,
)
from story_master.generators.environment_generation.interior_generator import (
    InteriorManager,
)
from story_master.generators.environment_generation.location_generator import (
    LocationGenerator,
)

from story_master.log import logger
from story_master.settings import Settings
from story_master.generators.environment_generation.map_creator import MapCreator
from story_master.storage.map.map_model import BaseLocation
from story_master.generators.environment_generation.populate_location import (
    LocationPopulationManager,
)
from story_master.storage.storage_manager import Sim, StorageManager
from story_master.storage.summary import SummaryAgent


class GameInitializer:
    def __init__(
        self,
        summary_agent: SummaryAgent,
        storage_manager: StorageManager,
        llm_model: BaseChatModel,
        settings: Settings,
    ):
        self.settings = settings
        self.summary_agent = summary_agent
        self.storage_manager = storage_manager
        self.location_generator = LocationGenerator(llm_model)
        self.character_generator = CharacterGenerator(
            llm_model, summary_agent, storage_manager
        )
        self.population_manager = LocationPopulationManager(llm_model)
        self.interior_manager = InteriorManager(llm_model)
        self.map_creator = MapCreator(llm_model, summary_agent, storage_manager)

    def pick_starting_location(self) -> BaseLocation:
        pass

    def generate_interior(self, location: BaseLocation) -> BaseLocation:
        location_summary = self.summary_agent.summarize_location(
            "Extract any information that can be relevant to the interior or object details, like doors, chests, trees, ...",
            location,
        )
        grid_objects = self.interior_manager.generate_interior(location_summary)
        location.environment_parts = grid_objects
        return location

    def initialize_game(self):
        if not self.storage_manager.map.locations:
            self.map_creator.create_map()
        exit()

        player_id = self.settings.main_player_id
        if player_id not in self.storage_manager.character_storage.player_characters:
            starting_location = self.pick_starting_location()
            characters = self.storage_manager.get_location_characters(starting_location)
            if len(characters) < 1:
                print("populating the area")
                location_description = self.summary_agent.summarize_location(
                    "Extract any information that can be useful to define what characters can be found in this location",
                    starting_location,
                )
                character_descriptions = self.population_manager.generate(
                    location_description, characters
                )
                for description in character_descriptions:
                    location_description = self.summary_agent.summarize_location(
                        f"Extract any information that can be useful to create the following character {description}",
                        starting_location,
                    )
                    character = self.character_generator.generate(
                        description, False, location_description
                    )
                    print("Generated", character.name)
                    self.storage_manager.add_character(
                        character, False, starting_location.id
                    )

            print("Generating new character for the player")
            main_character_description = "A great leader from the dwarven kingdom. He is a master of the axe and a great strategist."
            location_description = self.summary_agent.summarize_location(
                f"Extract any information that can be useful to create the following character {main_character_description}",
                starting_location,
            )
            character = self.character_generator.generate(
                main_character_description,
                True,
                location_description,
            )

            main_player = Sim(
                id=player_id,
                character=character,
                memories=[],
                current_location_id=starting_location.id,
            )
            self.storage_manager.character_storage.player_characters[player_id] = (
                main_player
            )
            self.storage_manager.save_characters()
        main_player = self.storage_manager.get_sim(player_id)
        location = self.storage_manager.get_location(main_player.current_location_id)

        if not location.environment_parts:
            logger.info("Generating interior")
            location = self.generate_interior(location)
            self.storage_manager.save_map()
