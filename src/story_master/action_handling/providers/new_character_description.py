from langchain_core.language_models.chat_models import BaseChatModel

from story_master.action_handling.parameter import Parameter, FilledParameter
from story_master.action_handling.providers.provider import Provider
from story_master.generators.character_generation.description_generator import (
    CharacterDescriptionGenerator,
)
from story_master.storage.storage_manager import StorageManager
from story_master.storage.summary import SummaryAgent


class CharacterDescriptionProvider(Provider):
    def __init__(
        self,
        llm_model: BaseChatModel,
        summary_agent: SummaryAgent,
        storage_manager: StorageManager,
    ):
        super().__init__(llm_model, summary_agent, storage_manager)
        self.character_description_generator = CharacterDescriptionGenerator(llm_model)

    def get_description(self) -> str:
        return "Generate the description for a new character"

    def get_input_parameters(self) -> dict[str, Parameter]:
        return {
            "location_id": Parameter(
                name="location_id",
                description="The location where the character should be created",
            ),
            "intent": Parameter(
                name="intent",
                description="The intent for the action",
            ),
        }

    def get_output_parameters(self) -> dict[str, Parameter]:
        return {
            "new_character_description": Parameter(
                name="new_character_description",
                description="The description of the character that needs to be generated",
            )
        }

    def execute(
        self, location_id: int, intent: str, **kwargs
    ) -> dict[str, FilledParameter]:
        location = self.storage_manager.get_location(location_id)
        location_description = self.summary_agent.summarize_location(
            f"Extract information that can be useful for generating a character for the following intent: {intent}",
            location,
        )
        character_description = self.character_description_generator.generate(
            intent, location_description
        )
        return {
            "new_character_description": FilledParameter(
                name="new_character_description",
                value=character_description,
                description="The description of the character that needs to be generated",
            )
        }
