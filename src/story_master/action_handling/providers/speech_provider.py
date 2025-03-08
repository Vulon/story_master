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


class SpeechProvider(Provider):
    PROMPT = """
    You are an agent for the simulation game

    -Goal-
    Write a speech that the character will say.
    
    -Steps-
    1. Analyze the character's plan.
    2. Analyze the target character.
    3. Analyze the speaker.
    4. Generate a speech for the character.
    
    -Plan-
    {plan}
    
    -Speaker-
    {speaker_description}
    
    -Target-
    {target_description}
    
    -Output format-
    <Speech>Speech</Speech>
    
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
        self.output_pattern = re.compile(r"<.?Speech.?>(.*?)</.?Speech.?>")

    def get_description(self) -> str:
        return "Generate a speech for a character"

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
            "target_character_id": Parameter(
                name="target_character_id",
                description="The target character for the action",
            ),
        }

    def get_output_parameters(self) -> dict[str, Parameter]:
        return {
            "speech": Parameter(
                name="speech",
                description="The speech to be spoken by the character",
            ),
        }

    def parse_output(self, raw_output: str) -> str:
        try:
            raw_output = raw_output.replace("\n", " ").strip()
            speech = self.output_pattern.search(raw_output).group(1)
            return speech
        except Exception:
            logger.error(f"Failed to parse output: {raw_output}")
            raise ValueError("Invalid output format")

    def execute(
        self,
        target_parameter: Parameter,
        actor_character_id: int = None,
        plan: str = None,
        target_character_id: int = None,
        **kwargs,
    ) -> dict[str, FilledParameter]:
        assert actor_character_id is not None
        assert plan is not None
        assert target_character_id is not None

        actor = self.storage_handler.get_sim(actor_character_id)
        target = self.storage_handler.get_sim(target_character_id)

        actor_description = actor.character.get_self_description()
        target_description = self.memory_handler.get_sim_description(actor, target)
        speech = self.chain.invoke(
            {
                "plan": plan,
                "speaker_description": actor_description,
                "target_description": target_description,
            }
        )
        return {
            "speech": FilledParameter(
                name="speech",
                value=speech,
                description="The speech to be spoken by the character",
            )
        }
