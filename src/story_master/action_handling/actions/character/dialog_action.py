from story_master.action_handling.actions.action import Action
import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.action_handling.parameter import Parameter
from story_master.log import logger
from story_master.storage.storage_manager import StorageManager
from story_master.storage.summary import SummaryAgent


from story_master.generators.make_observation import ObservationAgent


class DialogAction(Action):
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Generate a response in a dialog between the main character and a dialog responder.

    -Steps-
    1. Read the main character intention.
    2. Read the description of the main character
    3. Read the description of the dialog responder.
    4. Read the memory of the dialog responder.
    5. Read the description of the location.
    6. Generate a response from the perspective of the dialog responder.
    7. Output the response:
        Format: <Response>Response</Response>

    -Main character intention-
    {main_character_intention}

    -Main character description-
    {main_character_description}

    -Dialog responder description-
    {dialog_responder_description}

    -Dialog responder memory-
    {dialog_responder_memory}

    -Location description-
    {location_description}

    ########
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
        self.pattern = re.compile(r"<Response>(.*?)</Response>")
        self.chain = self.prompt | llm_model | StrOutputParser() | self.parse_output

        self.observation_agent = ObservationAgent(storage_manager, llm_model)

    def parse_output(self, output: str) -> str:
        try:
            print("Response:", output)
            output = output.replace("\n", " ")
            match = self.pattern.search(output)
            return match.group(1)
        except Exception as e:
            logger.error(f"DialogAction. Failed to parse output: {output}")
            raise e

    def execute(
        self,
        intent: str,
        actor_character_id: int,
        location_id: int,
        responder_character_id: int,
        **kwargs,
    ):
        actor = self.storage_manager.get_sim(actor_character_id)
        target = self.storage_manager.get_sim(responder_character_id)
        location = self.storage_manager.get_location(location_id)

        actor_description = f"{actor.character.get_stranger_description()}. Status: {actor.current_status}."
        if actor.id in target.character_relations:
            actor_description += (
                f" Previous relations: {target.character_relations[actor.id]}."
            )

        target_description = self.summary_agent.get_summary(
            f"Extract any information that can be relevant to create a response to the following intent: {intent}",
            f"Character information: {target.character.get_description()}. Status: {target.current_status}.",
        )

        target_memories = self.summary_agent.summarize_memories(
            f"Extract any information that can be relevant to create a response to the following intent: {intent}",
            self.storage_manager.get_memories(
                f"Dialog with {actor.character.name}. Intent: {intent}", target
            ),
        )

        location_description = self.summary_agent.get_summary(
            f"Extract any information that can be relevant for this character's speech: {intent}",
            f"Location information: {location.get_description()}.",
        )

        target_response = self.chain.invoke(
            {
                "main_character_intention": intent,
                "main_character_description": actor_description,
                "dialog_responder_description": target_description,
                "dialog_responder_memory": target_memories,
                "location_description": location_description,
            }
        )
        context = f"""
        {actor.character.name} is saying: {intent}.
        {target.character.name} is responding: {target_response}.
        """
        logger.info(f"Context: {context}")

        if target.id in actor.character_relations:
            relations_string = (
                actor.character_relations[target.id]
                + f" I said: {intent}. They responded: {target_response}."
            )
            relations_string = self.summary_agent.get_summary(
                "Summarize relations", relations_string
            )
        else:
            relations_string = f"I said: {intent}. They responded: {target_response}."
        actor.character_relations[target.id] = relations_string

        if actor.id in target.character_relations:
            relations_string = (
                target.character_relations[actor.id]
                + f" They said: {intent}. I responded: {target_response}."
            )
            relations_string = self.summary_agent.get_summary(
                "Summarize relations", relations_string
            )
        else:
            relations_string = f"They said: {intent}. I responded: {target_response}."
        target.character_relations[actor.id] = relations_string

        self.observation_agent.run(
            actor, context, location_description=location_description
        )
        self.observation_agent.run(
            target, context, target_memories, location_description
        )
        actor.current_status = f"In a dialog with {target.character.name}."
        target.current_status = f"In a dialog with {actor.character.name}."

        logger.info(f"Actor memory {actor.memories[-1].content}")
        logger.info(f"Responder memory {target.memories[-1].content}")
        self.storage_manager.save_characters()

    def get_description(self) -> str:
        return "Generate a response in a dialog between the main character and a dialog responder."

    def get_parameters(self) -> dict[str, Parameter]:
        return {
            "intent": Parameter(name="intent", description="Intent for the action"),
            "actor_character_id": Parameter(
                name="actor_character_id",
                description="ID of the character associated with the action",
            ),
            "location_id": Parameter(
                name="location_id",
                description="ID of the location where the dialog is happening",
            ),
            "responder_character_id": Parameter(
                name="responder_character_id",
                description="ID of the character who is responding to the main character",
            ),
        }
