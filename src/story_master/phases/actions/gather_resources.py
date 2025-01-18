import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from datetime import timedelta

from story_master.entities.items.resources import RESOURCES, Resource
from story_master.graphs.environment_generation.interior_generator import (
    InteriorGenerator,
)
from story_master.storage.storage_models import Sim
from story_master.settings import Settings
from story_master.storage.map.map_model import Location

from story_master.storage.storage_manager import StorageManager
from story_master.storage.storage_models import ResourceGatheredEvent
from difflib import get_close_matches


class ResourceGatheringAgent:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-    
    Handle the character's intent to gather resources.
    
    -Steps-
    1. Read the character's intent.
    2. Read the description of the location.
    3. Read character's description
    4. Read character's memories
    5. Identify the resource, that the character wants to gather.
        Pick the resource from the list of resources.
    6. Decide how much resources in pounds the character will gather in one session.
        Write a single float number.
    7. Decide how much time the character will spend gathering resources.
        Write a single float number, that represents the number of hours.
    8. Output the information in XML format:       
        <Resource>Resource name</Resource>
        <Amount>Amount in pounds</Amount>
        <Time>Time in hours</Time>
        
    -Character intent-
    {character_intent}
    
    -Location description-
    {location_description}
    
    -Character description-
    {character_description}
    
    -Character memories-
    {character_memories}
    
    -List of resources-
    {list_of_resources}
    
    -Output format-
    <Resource>Resource name</Resource>
    <Amount>Amount in pounds</Amount>
    <Time>Time in hours</Time>
    
    ########
    Output:
    """

    def __init__(
            self,
            llm_model: BaseChatModel,
            storage_manager: StorageManager,
    ):
        self.storage_manager = storage_manager
        self.prompt = PromptTemplate.from_template(self.PROMPT)
        self.resource_pattern = re.compile(r"<Resource>(.*?)</Resource>")
        self.amount_pattern = re.compile(r"<Amount>(.*?)</Amount>")
        self.time_pattern = re.compile(r"<Time>(.*?)</Time>")
        self.list_of_resources = [
            str(resource) for resource in
            RESOURCES.keys()
        ]
        self.chain = self.prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> tuple[Resource, float, timedelta]:
        output = output.replace("\n", " ")
        resource_match = self.resource_pattern.search(output)
        amount_match = self.amount_pattern.search(output)
        time_match = self.time_pattern.search(output)

        raw_resource = resource_match.group(1)
        raw_resource = get_close_matches(raw_resource, self.list_of_resources)[0]
        resource = RESOURCES[raw_resource]

        amount = float(amount_match.group(1))
        time = timedelta(hours=float(time_match.group(1)))

        return resource, amount, time


    def run(self, sim: Sim, character_intentions: str):
        location = self.storage_manager.get_location(sim.current_location_id)
        memories = self.storage_manager.get_memories(character_intentions, sim)

        memories_string = self.storage_manager.format_memories(memories)
        location_description = location.get_full_description()
        character_description = sim.character.get_description()

        resource, amount, time = self.chain.invoke({
            "character_intent": character_intentions,
            "location_description": location_description,
            "character_description": character_description,
            "character_memories": memories_string,
            "list_of_resources": self.list_of_resources,
        })
        return resource, amount, time
