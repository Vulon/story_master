import re

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from story_master.action_handling.parameter import Parameter, FilledParameter
from story_master.action_handling.providers.provider import Provider
from story_master.entities.handlers.event_handler import EventHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.entities.handlers.observation_handler import ObservationHandler
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.log import logger

DEFAULT_SEARCH_RADIUS = 10


class TargetCharacterProvider(Provider):
    PROMPT = """
    You are an agent for the simulation game
    
    -Goal-
    Find the character that the action should target
    
    -Steps-
    1. Analyze the list of characters
    2. Analyze the intention and the details of the action.
    3. Find the character that the action should target. 
        Output the character's ID - a single integer.
        
    -Intention-
    {intention}
    
    -Action details-
    {action_details}
    
    -Available characters-
    {characters}
    
    -Output format-
    <Character>Character ID</Character>
    Output:    
    """

    def __init__(
        self,
        llm_model: BaseChatModel,
        summary_handler: SummaryHandler,
        storage_handler: StorageHandler,
        observation_handler: ObservationHandler,
        memory_handler: MemoryHandler,
        event_handler: EventHandler,
    ):
        super().__init__(
            llm_model,
            summary_handler,
            storage_handler,
            observation_handler,
            memory_handler,
            event_handler,
        )
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | self.llm_model | StrOutputParser() | self.parse_output
        self.output_pattern = re.compile(r"<Character>(.*?)</Character>")

    def get_description(self) -> str:
        return "Finds a target character for the action"

    def get_input_parameters(self) -> dict[str, Parameter]:
        return {
            "actor_character_id": Parameter(
                description="The ID of the character who is speaking",
                name="actor_character_id",
            ),
            "plan": Parameter(
                name="plan",
                description="The plan of the character",
            ),
        }

    def get_output_parameters(self) -> dict[str, Parameter]:
        return {
            "target_character_id": Parameter(
                name="target_character_id",
                description="The target character for the action",
            ),
        }

    def parse_output(self, raw_output: str) -> int:
        try:
            raw_output = raw_output.replace("\n", " ").strip()
            raw_id = self.output_pattern.search(raw_output).group(1)
            character_id = int(re.search(r"\d+", raw_id).group(0))
            return character_id
        except Exception:
            logger.error(f"Failed to parse output: {raw_output}")
            raise ValueError("Invalid output format")

    def execute(
        self,
        target_parameter: Parameter,
        actor_character_id: int = None,
        plan: str = None,
        **kwargs,
    ) -> dict[str, FilledParameter]:
        assert actor_character_id is not None
        assert plan is not None

        actor = self.storage_handler.get_sim(actor_character_id)
        nearby_characters = self.storage_handler.get_sims(
            actor.position, radius=DEFAULT_SEARCH_RADIUS
        )
        if len(nearby_characters) == 0:
            raise ValueError("No characters found nearby")
        character_descriptions = []
        for sim in nearby_characters:
            name = self.memory_handler.get_sim_name(actor, sim)
            if not name:
                name = self.memory_handler.get_sim_description(actor, sim)
            character_descriptions.append(f"(ID {sim.id}: {name})")
        action_details = target_parameter.description

        raw_character_id = self.chain.invoke(
            {
                "intention": plan,
                "action_details": action_details,
                "characters": "\n".join(character_descriptions),
            }
        )
        character_ids = {sim.id for sim in nearby_characters}
        if raw_character_id not in character_ids:
            raise ValueError("Invalid character ID")
        return {
            "target_character_id": FilledParameter(
                name="target_character_id",
                value=raw_character_id,
                description="The target character for the action",
            )
        }
