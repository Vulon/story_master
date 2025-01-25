from story_master.action_handling.actions.action import Action
from story_master.graphs.character_generation.character_generator import (
    CharacterGenerator,
)
from langchain_core.language_models.chat_models import BaseChatModel
from story_master.action_handling.parameter import Parameter

from story_master.storage.storage_manager import StorageManager
from story_master.storage.summary import SummaryAgent


class CreateCharacterAction(Action):
    def __init__(
        self,
        llm_model: BaseChatModel,
        summary_agent: SummaryAgent,
        storage_manager: StorageManager,
    ):
        super().__init__(llm_model, summary_agent, storage_manager)
        self.character_generator = CharacterGenerator(
            llm_model, summary_agent, storage_manager
        )

    def execute(self, location_id: int, new_character_description: str, **kwargs):
        location = self.storage_manager.get_location(location_id)
        location_description = self.summary_agent.summarize_location(
            f"Extract any information that can be used to create the following character: {new_character_description}",
            location,
        )
        character = self.character_generator.generate(
            new_character_description, False, location_description
        )
        self.storage_manager.add_character(character, False, location_id)

    def get_description(self) -> str:
        return "Create a new character in a location"

    def get_parameters(self) -> dict[str, Parameter]:
        return {
            "new_character_description": Parameter(
                name="new_character_description",
                description="The description of the character that needs to be generated",
            ),
            "location_id": Parameter(
                name="location_id",
                description="The location where the character should be created",
            ),
        }
