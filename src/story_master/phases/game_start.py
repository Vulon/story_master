from langchain_core.language_models.chat_models import BaseChatModel

from story_master.graphs.character_generation.character_generator import (
    CharacterGenerator,
)
from story_master.graphs.environment_generation.decomposer import LocationDecomposer
from story_master.graphs.environment_generation.location_generator import (
    LocationGenerator,
)
from story_master.graphs.environment_generation.location_selector import (
    LocationSelector,
)
from story_master.graphs.environment_generation.route_generator import RouteGenerator
from story_master.settings import Settings
from story_master.storage.map.map_model import Location
from story_master.graphs.environment_generation.populate_location import (
    LocationPopulationManager,
)
from story_master.storage.storage_manager import Sim, StorageManager


class GameInitializer:
    def __init__(
        self,
        storage_manager: StorageManager,
        llm_model: BaseChatModel,
        settings: Settings,
    ):
        self.settings = settings
        self.storage_manager = storage_manager
        self.location_selector = LocationSelector(llm_model)
        self.location_generator = LocationGenerator(llm_model)
        self.location_decomposer = LocationDecomposer(llm_model)
        self.character_generator = CharacterGenerator(llm_model)
        self.route_generator = RouteGenerator(llm_model)
        self.population_manager = LocationPopulationManager(llm_model)

    def pick_starting_location(self) -> Location:
        available_locations = [
            item
            for item in self.storage_manager.map.locations
            if item.parent_location == 0
        ]
        max_location_id = max([location.id for location in available_locations])
        iteration_counter = 0
        while True:
            print("While iteration", iteration_counter)
            location_names = [location.name for location in available_locations]
            print("Available locations:", location_names)
            task_description = "You need to pick a starting location for the DnD game"
            selected_location_name = self.location_selector.generate(
                location_names, task_description
            )
            print("Selected location:", selected_location_name)
            selected_location = [
                location
                for location in available_locations
                if location.name == selected_location_name
            ][0]
            available_locations = []
            if selected_location.is_leaf:
                return selected_location
            child_locations = self.storage_manager.get_child_locations(
                selected_location.id
            )
            if len(child_locations) == 0:
                new_location_names = self.location_decomposer.generate(
                    selected_location, location_names
                )
                print("New locations:", new_location_names)
                for new_name in new_location_names:
                    max_location_id += 1
                    new_location = self.location_generator.generate(
                        selected_location, new_name, max_location_id
                    )
                    print()
                    print("-" * 20)
                    print("New location:", new_location)
                    print("-" * 20)
                    print()
                    available_locations.append(new_location)
                print()
                print()
                new_routes = self.route_generator.generate(
                    available_locations, selected_location
                )
                print()
                print()
                self.storage_manager.map.locations.extend(available_locations)
                self.storage_manager.map.routes.extend(new_routes)
                self.storage_manager.save_map()
            else:
                available_locations = child_locations
            iteration_counter += 1

    def initialize_game(self):
        player_id = self.settings.main_player_id
        if player_id not in self.storage_manager.character_storage.player_characters:
            starting_location = self.storage_manager.get_location(12)
            print("Don't forget to remove this hardcoded location")
            print("!")
            # starting_location = self.pick_starting_location()
            characters = self.storage_manager.get_location_characters(starting_location)
            if len(characters) < 1:
                print("populating the area")
                character_descriptions = self.population_manager.generate(
                    starting_location, characters
                )
                print("Generated character descriptions:", character_descriptions)
                for description in character_descriptions:
                    character = self.character_generator.generate(
                        description, False, starting_location
                    )
                    print("Generated", character.name)
                    self.storage_manager.add_character(
                        character, False, starting_location.id
                    )
            print("Generating new character for the player")
            character = self.character_generator.generate(
                "A great leader from the dwarven kingdom. He is a master of the axe and a great strategist.",
                True,
                starting_location,
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
