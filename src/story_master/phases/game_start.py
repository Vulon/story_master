import random

from langchain_core.language_models.chat_models import BaseChatModel

from story_master.graphs.character_generation.character_generator import (
    CharacterGenerator,
)
from story_master.graphs.environment_generation.decomposer import LocationDecomposer
from story_master.graphs.environment_generation.location_generator import (
    LocationGenerator,
)
from story_master.graphs.environment_generation.draft_location_selector import (
    LocationSelector,
)
from story_master.graphs.environment_generation.route_generator import RouteGenerator
from story_master.settings import Settings
from story_master.storage.map.map_model import LargeArea, DetailedArea
from story_master.graphs.environment_generation.populate_location import (
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
        self.location_selector = LocationSelector(llm_model)
        self.location_generator = LocationGenerator(llm_model)
        self.location_decomposer = LocationDecomposer(llm_model)
        self.character_generator = CharacterGenerator(
            llm_model, summary_agent, storage_manager
        )
        self.route_generator = RouteGenerator(llm_model)
        self.population_manager = LocationPopulationManager(llm_model)

    def pick_starting_location(self) -> LargeArea | DetailedArea:
        game_map = self.storage_manager.map.locations
        root_location = game_map[self.storage_manager.map.root_location]
        available_locations = [
            game_map[location_id] for location_id in root_location.sub_locations
        ]

        iteration_counter = 0
        tree_path = [root_location]
        while True:
            print("While iteration", iteration_counter)
            selected_location = random.choice(available_locations)
            print("Selected location:", selected_location.name)
            if isinstance(selected_location, DetailedArea):
                return selected_location

            child_locations = [
                game_map[location_id] for location_id in selected_location.sub_locations
            ]
            tree_path.append(selected_location)
            print("Tree path:", [location.name for location in tree_path])

            if len(child_locations) == 0:
                new_location_names = self.location_decomposer.generate(
                    selected_location, tree_path
                )
                available_locations = []
                print("New locations:", new_location_names)
                for new_name in new_location_names:
                    new_location = self.location_generator.generate(
                        selected_location, new_name, max(game_map) + 1
                    )
                    game_map[new_location.id] = new_location
                    selected_location.sub_locations.append(new_location.id)
                    available_locations.append(new_location)

                new_routes = self.route_generator.generate(available_locations)
                print()
                self.storage_manager.map.routes.extend(new_routes)
                self.storage_manager.save_map()
            else:
                available_locations = child_locations
            iteration_counter += 1

    def initialize_game(self):
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
