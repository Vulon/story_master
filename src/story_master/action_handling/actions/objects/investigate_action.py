import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.action_handling.actions.action import Action
from story_master.action_handling.parameter import Parameter
from story_master.generators.make_observation import ObservationAgent
from story_master.log import logger
from story_master.storage.storage_manager import StorageManager
from story_master.storage.summary import SummaryAgent


class InvestigateAction(Action):
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Handle the action of investigating an object in a location
    
    -Steps-
    1. Read the description of the location.
    2. Read the description of the object that needs to be investigated.
    3. Read the description of the character that is investigating the object.
    4. Read the memory of the character.
    5. Decide the information that the character can find by investigating the object.
        The object can have a hidden information that can be revealed by investigating it.
        You can also come up with a new information that the character can find.
    6. Output the information that the character finds by investigating the object.
    7. If you want to add hidden information, you can write it separately.
    
    -Location description-
    {location_description}
    
    -Object description-
    {object_description}
    
    -Character description-
    {character_description}
    
    -Character memory-
    {character_memory}
    
    -Output format-
    <Information> Information </Information>
    <HiddenInformation> Hidden information </HiddenInformation> (Optional)
    """

    def __init__(
        self,
        llm_model: BaseChatModel,
        summary_agent: SummaryAgent,
        storage_manager: StorageManager,
    ):
        super().__init__(llm_model, summary_agent, storage_manager)
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output
        self.output_pattern = re.compile(r"<Information>(.*?)</Information>")
        self.hidden_output_pattern = re.compile(
            r"<HiddenInformation>(.*?)</HiddenInformation>"
        )
        self.observation_agent = ObservationAgent(storage_manager, llm_model)

    def parse_output(self, output: str) -> tuple[str, str]:
        try:
            output = output.replace("\n", " ")
            match = self.output_pattern.search(output)
            information = match.group(1)
            hidden_information = ""
            hidden_match = self.hidden_output_pattern.search(output)
            if hidden_match:
                hidden_information = hidden_match.group(1)
            return information, hidden_information
        except Exception as e:
            logger.error(f"InvestigateAction. Error while parsing output: {output}")
            raise e

    def execute(
        self,
        target_object_id: int,
        intent: str,
        actor_character_id: int,
        location_id: int,
        **kwargs,
    ):
        actor = self.storage_manager.get_sim(actor_character_id)
        location = self.storage_manager.get_location(location_id)

        if target_object_id is None:
            logger.error("InvestigateAction. Target object ID is None.")
            self.observation_agent.run(
                actor, f"Couldn't find the object to investigate. Intent: {intent}"
            )
            return

        target_object = [
            part for part in location.environment_parts if part.id == target_object_id
        ][0]

        object_description = f"{target_object.get_description()} Hidden description: {target_object.hidden_description}"
        key = location_id, target_object_id

        if (object_memory := actor.get_object_memory(*key)) is not None:
            object_description += f" Memory: {object_memory}"

        character_description = actor.character.get_description()
        character_description = self.summary_agent.get_summary(
            f"Extract information that can be relevant to investigating the object {target_object.name}. Intent: {intent}",
            character_description,
        )

        memories = self.storage_manager.get_memories(
            f"Investigate the object: {target_object.name}. Intent: {intent}", actor
        )
        memories_summary = self.summary_agent.summarize_memories(
            f"Extract information that can be helpful to investigate the object: {target_object.name}. Intent: {intent}",
            memories,
        )
        location_description = location.get_description()
        location_description = self.summary_agent.get_summary(
            f"Extract information that can be relevant to investigating the object {target_object.name}. Intent: {intent}",
            location_description,
        )

        logger.info("Investigate action.")
        logger.info(f"Location description: {location_description}")
        logger.info(f"Object description: {object_description}")
        logger.info(f"Character description: {character_description}")
        logger.info(f"Character memory: {memories_summary}")

        object_information, hidden_information = self.chain.invoke(
            {
                "location_description": location_description,
                "object_description": object_description,
                "character_description": character_description,
                "character_memory": memories_summary,
            }
        )
        logger.info(f"Object information: {object_information}")
        logger.info(f"Hidden information: {hidden_information}")
        if hidden_information:
            target_object.hidden_description = hidden_information
            self.storage_manager.save_map()
        actor.add_object_memory(location_id, target_object_id, object_information)
        self.observation_agent.run(
            actor,
            f"Investigated the object {target_object.name}. Intent: {intent}. Information: {object_information}",
            location_description=location_description,
        )
        actor.current_status = f"Investigating {target_object.name}"
        self.storage_manager.save_characters()

    def get_description(self) -> str:
        return "Investigate an object in a location"

    def get_parameters(self) -> dict[str, Parameter]:
        return {
            "intent": Parameter(
                name="intent",
                description="The intent for the action",
            ),
            "target_object_id": Parameter(
                name="target_object_id",
                description="The ID of the object that needs to be investigated",
            ),
            "location_id": Parameter(
                name="location_id",
                description="The location where the object is located",
            ),
            "actor_character_id": Parameter(
                name="actor_character_id",
                description="The ID of the character that is investigating the object",
            ),
        }
