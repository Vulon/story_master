import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.action_handling.parameter import Parameter, FilledParameter
from story_master.action_handling.providers.provider import Provider
from story_master.log import logger
from story_master.storage.storage_manager import StorageManager
from story_master.storage.map.map_model import EnvironmentPart
from story_master.storage.summary import SummaryAgent


class TargetObjectProvider(Provider):
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Identify the target object for the provided action or intent
    
    -Steps-
    1. Read the intent for the DnD agent. It should contain hints for identifying the target object.
    2. Read the description of the location. 
    3. Read the description of the objects present in the location.
        It should include the ID, description and location of each object.
    4. If the action is related to a character, read the description of the character.
    5. Find the object, which is the target for the provided action or intent.
    6. Output the ID of the target object.
    
    -Intent-
    {intent}
    
    -Location description-
    {location_description}
    
    -Objects-
    {objects_description}
    
    -Character description-
    {character_description}
    
    -Output format-
    <Object> Object ID (int) </Object>    
    """

    def __init__(
        self,
        llm_model: BaseChatModel,
        summary_agent: SummaryAgent,
        storage_manager: StorageManager,
    ):
        super().__init__(llm_model, summary_agent, storage_manager)
        self.prompt = PromptTemplate.from_template(self.PROMPT)
        self.object_pattern = re.compile(r"<Object>(.*?)</Object>")
        self.chain = self.prompt | llm_model | StrOutputParser()

    def parse_output(
        self, output: str, objects: list[EnvironmentPart]
    ) -> EnvironmentPart:
        try:
            object_match = self.object_pattern.search(output)
            object_string = object_match.group(1)
            object_string = re.search(r"(\d+)", object_string).group(1)
            object_id = int(object_string)
            return [obj for obj in objects if obj.id == object_id][0]
        except Exception as e:
            logger.error(f"TargetObjectProvider. Could not parse: {output}")
            raise e

    def format_objects(self, objects: list[EnvironmentPart]) -> str:
        return " ; ".join(
            [
                f"({obj.id}: {obj.name}, {obj.description}, {obj.position})"
                for obj in objects
            ]
        )

    def get_description(self) -> str:
        return "Identify the target object for the provided action or intent"

    def get_input_parameters(self) -> dict[str, Parameter]:
        return {
            "intent": Parameter(
                name="intent",
                description="The intent for the action",
            ),
            "location_id": Parameter(
                name="location_id",
                description="The ID of the location where the action is taking place",
            ),
        }

    def get_output_parameters(self) -> dict[str, Parameter]:
        return {
            "target_object_id": Parameter(
                name="target_object_id",
                description="The ID of the target object for the provided action or intent",
            )
        }

    def execute(
        self,
        intent: str,
        location_id: int,
        actor_character_id: int | None = None,
        **kwargs,
    ) -> dict[str, FilledParameter]:
        location = self.storage_manager.get_location(location_id)
        location_description = self.summary_agent.get_summary(
            f"Extract information that can be useful for identifying the target object for the following intent: {intent}",
            f"Location description: {location.name}: {location.description}",
        )
        objects = location.environment_parts
        objects_description = self.format_objects(objects)
        if actor_character_id is not None:
            actor = self.storage_manager.get_sim(actor_character_id)
            character_description = (
                f"Character description: {actor.character.get_worker_description()}"
            )
        else:
            character_description = "Character not provided"
        object_id = self.chain.invoke(
            {
                "intent": intent,
                "location_description": location_description,
                "objects_description": objects_description,
                "character_description": character_description,
            }
        )
        target_object = self.parse_output(object_id, objects)
        return {
            "target_object_id": FilledParameter(
                name="target_object_id",
                value=target_object.id,
                description="The ID of the target object for the provided action or intent",
            )
        }
