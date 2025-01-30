import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.action_handling.parameter import Parameter, FilledParameter
from story_master.action_handling.providers.provider import Provider
from story_master.log import logger
from story_master.storage.storage_manager import StorageManager
from story_master.storage.storage_models import Sim
from story_master.storage.summary import SummaryAgent


class ResponderCharacterProvider(Provider):
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Identify the character, who is the target for main character's action.


    -Steps-
    1. Read the intent for the DnD agent. It should contain hints for identifying the target character.
    2. Read the description of the main character.
    3. Read the description of the other characters, present in the scene.
        It should include the ID and short description of each character.
    4. Read the memory of the main character. It might contain information about the target character.
    5. Find the character, who is the target for the main character's action.
        An action can be anything like talking, trading, helping, etc.
    6. Output the ID of the target character.
    
    -Main character intention-
    {intent}
    
    -Main character description-
    {actor_character_description}
    
    -Characters-
    {characters_description}
    
    -Main character memory-
    {actor_character_memory}
    
    -Output format-
    <Responder>Character ID (int)</Responder> 
        
    Output:    
    """

    def __init__(
        self,
        llm_model: BaseChatModel,
        summary_agent: SummaryAgent,
        storage_manager: StorageManager,
    ):
        super().__init__(llm_model, summary_agent, storage_manager)
        self.prompt = PromptTemplate.from_template(self.PROMPT)
        self.responder_pattern = re.compile(r"<Responder>(.*?)</Responder>")
        self.chain = self.prompt | llm_model | StrOutputParser()

    def parse_output(self, output: str, sims: list[Sim]) -> Sim:
        try:
            responder_match = self.responder_pattern.search(output)
            responder_string = responder_match.group(1)
            responder_string = re.search(r"(\d+)", responder_string).group(1)
            responder_id = int(responder_string)
            responder = [sim for sim in sims if sim.id == responder_id][0]
            return responder
        except Exception as e:
            logger.error(
                f"ResponderCharacterProvider. Failed to parse output: {output}. Sim IDs: {[sim.id for sim in sims]}"
            )
            raise e

    def format_character(self, sim: Sim) -> str:
        return f"(ID: {sim.id}. {sim.character.get_worker_description()})"

    def format_characters(self, sims: list[Sim]) -> str:
        strings = []
        for sim in sims:
            strings.append(self.format_character(sim))
        characters_string = "<Characters>" + "; ".join(strings) + "</Characters>"
        return characters_string

    def get_description(self) -> str:
        return "Identify the character, who is the target for main character's action."

    def get_input_parameters(self) -> dict[str, Parameter]:
        return {
            "intent": Parameter(
                name="intent",
                description="The intent for the action",
            ),
            "actor_character_id": Parameter(
                name="actor_character_id",
                description="The main character, who makes the action",
            ),
        }

    def get_output_parameters(self) -> dict[str, Parameter]:
        return {
            "responder_character_id": Parameter(
                name="responder_character_id",
                description="The ID of the character, who is the target for the main character's action",
            )
        }

    def execute(
        self, intent: str, actor_character_id: int, **kwargs
    ) -> dict[str, FilledParameter]:
        actor = self.storage_manager.get_sim(actor_character_id)
        location = self.storage_manager.get_location(actor.current_location_id)
        sims = self.storage_manager.get_location_characters(location)
        sims = [sim for sim in sims if sim.id != actor_character_id]
        actor_memories = self.storage_manager.get_memories(intent, actor)
        actor_memory_description = self.summary_agent.summarize_memories(
            f"Information that can be used to find the target character for intent: {intent}",
            actor_memories,
        )

        location_character_description = self.format_characters(sims)
        actor_description = self.format_character(actor)

        raw_llm_output = self.chain.invoke(
            {
                "intent": intent,
                "actor_character_description": actor_description,
                "characters_description": location_character_description,
                "actor_character_memory": actor_memory_description,
            }
        )
        logger.info(f"Character finder output: {raw_llm_output}")
        responder = self.parse_output(raw_llm_output, sims)
        return {
            "responder_character_id": FilledParameter(
                name="responder_character_id",
                value=responder.id,
                description="The ID of the character, who is the target for the main character's action",
            )
        }
