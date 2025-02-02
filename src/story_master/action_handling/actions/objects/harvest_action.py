import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.action_handling.actions.action import Action
from story_master.action_handling.parameter import Parameter
from story_master.entities.items.items import ItemStack
from story_master.generators.make_observation import ObservationAgent
from story_master.log import logger
from story_master.storage.map.map_model import DetailedArea, EnvironmentPart
from story_master.storage.storage_manager import StorageManager
from story_master.storage.storage_models import Sim
from story_master.storage.summary import SummaryAgent
from story_master.entities.items.resources import RESOURCES
from difflib import get_close_matches


class ObjectHarvestHandler:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Handle the action of harvesting an object for resources
    
    -Steps-
    1. Read character's intent.
    2. Read the description of the location.
    3. Read the description of the character.
    4. Read the character's memories.
    5. Read the description of the object that the character wants to harvest.
    5. Identify, what resource the object can provide.
        Pick the resource from the provided list of resources.
    6. Decide how much resources in pounds the character will gather in one session.
        Write a single float number.
    7. Update the object's description. 
        Write the new description that will replace the old one.
        It should mention that the object has been harvested for resources.
    8. Decide, if the object will be destroyed after harvesting.
        Write "Yes" or "No".
    
    -Character intent-
    {character_intent}
    
    -Location description-
    {location_description}
    
    -Character description-
    {character_description}
    
    -Character memories-
    {character_memories}
    
    -Object description-
    {object_description}
    
    -List of resources-
    {list_of_resources}
    
    -Output format-
    <Resource>Resource name</Resource>
    <Amount>Amount in pounds</Amount>
    <ObjectDescription>Object description</ObjectDescription>
    <Destroy>Yes/No</Destroy>
        
    Output:    
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output
        self.resource_pattern = re.compile(r"<Resource>(.*?)</Resource>")
        self.amount_pattern = re.compile(r"<Amount>(.*?)</Amount>")
        self.object_description_pattern = re.compile(
            r"<ObjectDescription>(.*?)</ObjectDescription>"
        )
        self.destroy_pattern = re.compile(r"<Destroy>(.*?)</Destroy>")
        self.list_of_resources = [str(resource) for resource in RESOURCES.keys()]

    def parse_output(self, output: str) -> tuple[str, float, str | None, bool]:
        output = output.replace("\n", " ")
        try:
            resource_match = self.resource_pattern.search(output)
            raw_resource = resource_match.group(1)
            resource = get_close_matches(raw_resource, self.list_of_resources)[0]
            amount_match = self.amount_pattern.search(output)
            amount = float(amount_match.group(1))
        except Exception as e:
            logger.error(f"ObjectHarvestHandler. Could not parse: {output}")
            raise e
        object_description_match = self.object_description_pattern.search(output)
        object_description = (
            object_description_match.group(1) if object_description_match else None
        )
        destroy_match = self.destroy_pattern.search(output)
        destroy = False
        if destroy_match:
            destroy = True if destroy_match.group(1).lower() == "yes" else False
        return resource, amount, object_description, destroy

    def run(
        self,
        intent: str,
        location_description: str,
        character_description: str,
        character_memories: str,
        object_description: str,
        list_of_resources: list[str],
    ) -> tuple[str, float, str | None, bool]:
        resource, amount, object_description, destroy = self.chain.invoke(
            {
                "character_intent": intent,
                "location_description": location_description,
                "character_description": character_description,
                "character_memories": character_memories,
                "object_description": object_description,
                "list_of_resources": list_of_resources,
            }
        )
        return resource, amount, object_description, destroy


class HarvestAction(Action):
    def __init__(
        self,
        llm_model: BaseChatModel,
        summary_agent: SummaryAgent,
        storage_manager: StorageManager,
    ):
        super().__init__(llm_model, summary_agent, storage_manager)
        self.object_harvest_handler = ObjectHarvestHandler(llm_model)
        self.observation_agent = ObservationAgent(storage_manager, llm_model)
        self.list_of_resources = [str(resource) for resource in RESOURCES.keys()]

    def handle_object_harvest(
        self,
        intent: str,
        location: DetailedArea,
        actor: Sim,
        target_object: EnvironmentPart,
    ) -> tuple[str, float]:
        object_description = target_object.get_description()
        query = f"Extract information that can be relevant to harvesting the object {target_object.name} for resources. Intent: {intent}"
        key = location.id, target_object.id
        if (object_memory := actor.get_object_memory(*key)) is not None:
            object_description += f" Memory: {object_memory}"

        location_description = location.get_description()
        location_description = self.summary_agent.get_summary(
            query,
            location_description,
        )

        character_description = actor.character.get_description()
        character_description = self.summary_agent.get_summary(
            query,
            character_description,
        )

        memories = self.storage_manager.get_memories(
            f"Harvest {target_object.name} ({target_object.description}) for resources. Intent: {intent}",
            actor,
        )
        memories_summary = self.summary_agent.summarize_memories(query, memories)
        logger.info("Running object harvest handler")
        logger.info(f"Intent: {intent}")
        logger.info(f"Location description: {location_description}")
        logger.info(f"Character description: {character_description}")
        logger.info(f"Character memory: {memories_summary}")
        logger.info(f"Object description: {object_description}")

        resource, amount, object_description, destroy = self.object_harvest_handler.run(
            intent,
            location_description,
            character_description,
            memories_summary,
            object_description,
            self.list_of_resources,
        )
        logger.info(f"Resource: {resource}")
        logger.info(f"Amount: {amount}")
        logger.info(f"Object description: {object_description}")
        logger.info(f"Destroy: {destroy}")

        actor.add_object_memory(
            location.id,
            target_object.id,
            f"Gathered {target_object.name}. Extracted {amount} pounds of {resource}",
        )

        observation_context = f"Harvested {target_object.name} for resources.  Extracted {amount} pounds of {resource}"
        if object_description:
            target_object.description = object_description
        if destroy:
            location.environment_parts.remove(target_object)
            observation_context += f". Destroyed {target_object.name}"
            actor.delete_object_memory(location.id, target_object.id)
        self.observation_agent.run(
            actor, observation_context, location_description=location.name
        )
        actor.current_status = f"Harvesting {target_object.name} for {resource}"
        self.storage_manager.save_map()
        self.storage_manager.save_characters()
        return resource, amount

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
            raise NotImplementedError("HarvestAction. Target object ID is None.")
        else:
            target_object = [
                part
                for part in location.environment_parts
                if part.id == target_object_id
            ][0]
            logger.info(
                f"Harvesting object {target_object.name} in location {location.name}"
            )
            resource_name, amount = self.handle_object_harvest(
                intent, location, actor, target_object
            )

        resource = RESOURCES[resource_name]
        if resource_name in actor.character.items:
            actor.character.items[resource_name].quantity += amount
        else:
            actor.character.items[resource_name] = ItemStack(
                item=resource, quantity=amount
            )
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
                description="The ID of the object to harvest",
            ),
            "location_id": Parameter(
                name="location_id",
                description="The location where the object is located",
            ),
            "actor_character_id": Parameter(
                name="actor_character_id",
                description="The ID of the character that is harvesting the object",
            ),
        }
