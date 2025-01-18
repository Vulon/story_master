import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.graphs.environment_generation.interior_generator import (
    InteriorGenerator,
)
from story_master.storage.storage_models import Sim
from story_master.settings import Settings
from story_master.storage.map.map_model import Location
from story_master.storage.memory.memory_model import Observation
from story_master.storage.storage_manager import StorageManager


class LookAroundAgent:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Tell the character what they see around them.

    -Steps-
    1. Read the description of the location.
    2. Read the list of character already present in location if they exist.
    3. Read the description of the character.
    4. Read the character's memories.
    5. Read the character's situation.
    6. Read character's intentions, what they want to see around them.    
    7. Answer the character's question about the location or the people in it.
        Output the description in XML format.
        Format: <Environment>Environment description</Environment>
        The description should be in English.        
    All your text should be in <Environment> and </Environment> tags, it should be written in natural language without any tags.
    Don't write anything else in the output.
    
    
    -Character intentions-
    {character_intentions}    

    -Location description-
    {location_description}

    -Character description-
    {character_description}

    -Character memories-
    {character_memories}

    -Character situation-
    {character_situation}
    
    -Characters already present-
    {existing_characters}
    
    -Output format-
    <Environment>Environment description</Environment>
    
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
        self.pattern = re.compile(r"<Environment>(.*?)</Environment>")
        self.chain = self.prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> str:
        output = output.replace("\n", " ")
        match = self.pattern.search(output)
        location_description = match.group(1)
        return location_description

    def format_memories(self, memories: list[Observation]) -> str:
        strings = []
        for memory in memories:
            strings.append(f"{memory.title}: {memory.content}")
        memories_string = "<Memories>" + "; ".join(strings) + "</Memories>"
        return memories_string

    def format_existing_characters(self, location_characters: list[Sim]) -> str:
        strings = []
        for sim in location_characters:
            strings.append(
                f"{sim.character.name}: {sim.character.type}"
                f", Status: {sim.current_status or 'Not defined'}"
            )
        characters_string = "<Characters>" + "; ".join(strings) + "</Characters>"
        return characters_string

    def run(self, sim: Sim, character_intentions: str):
        location = self.storage_manager.get_location(sim.current_location_id)
        location_characters = self.storage_manager.get_location_characters(location)
        characters_string = self.format_existing_characters(location_characters)
        memories_string = self.format_memories(sim.memories)
        area_description = self.chain.invoke(
            {
                "location_description": location.get_full_description(),
                "character_description": sim.character.get_description(),
                "character_memories": memories_string,
                "character_situation": sim.current_status or "",
                "character_intentions": character_intentions,
                "existing_characters": characters_string
            }
        )
        return area_description