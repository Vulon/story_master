import re
from enum import StrEnum

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.action_handling.actions.action import Action
from story_master.action_handling.parameter import Parameter
from story_master.generators.make_observation import ObservationAgent
from story_master.log import logger
from story_master.storage.storage_manager import StorageManager
from story_master.storage.summary import SummaryAgent

class CraftItemType(StrEnum):
    WEAPON = "Weapon"
    ARMOR = "Armor"
    FURNITURE = "Furniture"
    CLOTHING = "Clothing"
    OTHER = "Other"

class ItemTypeIdentifier:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Identify the type of item that the character wants to craft.
    
    -Steps-
    1. Read the character's intent.
    2. Read character's description.
    3. Read the description of the location.
    4. Read the character's memories.
    5. Identify the type of item that the character wants to craft.
        Select the type of item from the list of available types.
        
    -Character intent-    
    {character_intent}
    
    -Character description-
    {character_description}
    
    -Location description-
    {location_description}
    
    -Character memories-
    {character_memories}
    
    -List of item types-
    1. "Weapon" - character wants to craft a weapon.
    2. "Armor" - character wants to craft an armor (Including shields).
    3. "Furniture" - character wants to craft a piece furniture (Table, chair, bowl, chest, etc).
    4. "Clothing" - character wants to craft a piece of clothing (Robe, cloak, shirt, etc).
    5. "Other" - character wants to craft an item that does not fit into the above categories.
    
    -Output format-
    <ItemType> Item type </ItemType>
    
    Output
    """

    def __init__(self, llm_model: BaseChatModel):
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output
        self.output_pattern = re.compile(r"<ItemType>(.*?)</ItemType>")

    def parse_output(self, output: str) -> CraftItemType:
        try:
            match = self.output_pattern.search(output)
            item_type = match.group(1)
            return CraftItemType(item_type)
        except Exception as e:
            logger.error(f"ItemTypeIdentifier. Failed to parse output: {output}")
            raise e

    def handle(self, character_intent: str, character_description: str, location_description: str, character_memories: str) -> CraftItemType:
        output = self.chain.invoke({
            "character_intent":character_intent,
            "character_description": character_description,
            "location_description": location_description,
            "character_memories": character_memories,
        })
        return output



class CraftItemAction(Action):

    def __init__(
            self,
            llm_model: BaseChatModel,
            summary_agent: SummaryAgent,
            storage_manager: StorageManager,
    ):
        super().__init__(llm_model, summary_agent, storage_manager)
        self.observation_agent = ObservationAgent(storage_manager, llm_model)

    def execute(
            self,
            intent: str,
            actor_character_id: int,
            location_id: int,
            **kwargs,
    ):
        actor = self.storage_manager.get_sim(actor_character_id)
        location = self.storage_manager.get_location(location_id)

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
            "location_id": Parameter(
                name="location_id",
                description="The location where the object is located",
            ),
            "actor_character_id": Parameter(
                name="actor_character_id",
                description="The ID of the character that is investigating the object",
            ),
        }
