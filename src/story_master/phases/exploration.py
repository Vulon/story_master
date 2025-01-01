import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.graphs.environment_generation.interior_generator import (
    InteriorGenerator,
)
from story_master.settings import Settings
from story_master.storage.map.map_model import Location
from story_master.storage.memory.memory_model import Observation
from story_master.storage.storage_manager import StorageManager


class ExplorationAgent:
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Handle character's actions during exploration.
    
    -Steps-
    1. Read the description of the location.
    2. Read the description of the character.
    3. Read the character's actions.
        The character's actions will be written in the first person.
    4. Read recent character's memories.
    5. Read current character's situation description.
    6. Create an observation of what is happening as the result of the character's actions.
    7. Output the observation.
        You need to fill the following fields:
        title: title of the observation
        content: content of the observation. It should be detailed enough to allow the player to understand what is happening.
        importance: importance of the observation: 1-5
        Every field should be in a separate XML tag.
        Output every field in a separate line.
    8. Output the change in location. 
        You will receive the current description of the location.
        It will include the name of the location, description and interior.
        You need to write any changes that happened to the interior.
        If nothing changed, don't output the Location tag.
        If there are changes in the interior, output the new interior description in the following format:
        <Location>
        New location interior description
        </Location>
    9. Output the new character status. 
        You will receive the current character status if it exists.
        You need to write a new description of what is happening to the character.
        You can write where the character is, what the character is doing, etc.        
        Output the new character status in the following format:
        <CharacterStatus>
        New detailed character status
        </CharacterStatus>
    Output only one observation, location change, and character status.
    Even if the character triggered multiple events, handle only the first one.
    
    -Location description-
    {location_description}
    
    -Character description-
    {character_description}
    
    -Character memories-
    {character_memories}
    
    -Character situation-
    {character_situation}
    
    -Character actions-
    {character_actions}
    
    -Example output-
    <Title>Character found a hidden chest</Title>
    <Content>The character found a hidden chest behind the painting.</Content>
    <Importance>5</Importance>
    <Location>
    The room is now filled with light.
    </Location>
    <CharacterStatus>
    The character is now looking at the chest.
    </CharacterStatus>
    ########
    Output:
    """

    def __init__(
        self,
        storage_manager: StorageManager,
        llm_model: BaseChatModel,
        settings: Settings,
    ):
        self.settings = settings
        self.storage_manager = storage_manager
        self.prompt = PromptTemplate.from_template(self.PROMPT)
        self.title_pattern = re.compile(r"<Title>(.*?)</Title>")
        self.content_pattern = re.compile(r"<Content>(.*?)</Content>")
        self.importance_pattern = re.compile(r"<Importance>(.*?)</Importance>")
        self.location_pattern = re.compile(r"<Location>(.*?)</Location>")
        self.status_pattern = re.compile(r"<CharacterStatus>(.*?)</CharacterStatus>")
        self.chain = self.prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str):
        output = output.replace("\n", " ")
        print("Raw memory output", output)
        title = self.title_pattern.search(output).group(1)
        content = self.content_pattern.search(output).group(1)
        importance = int(self.importance_pattern.search(output).group(1))
        location_match = self.location_pattern.search(output)
        location_description = location_match.group(1) if location_match else None
        status_match = self.status_pattern.search(output)
        status_description = status_match.group(1) if status_match else None
        return title, content, importance, location_description, status_description

    def format_memories(self, memories: list[Observation]) -> str:
        strings = []
        for memory in memories:
            strings.append(f"{memory.title}: {memory.content}")
        return "; ".join(strings)

    def run(self, character_actions: str):
        player = self.storage_manager.character_storage.player_characters[
            self.settings.main_player_id
        ]
        current_location = self.storage_manager.get_location(player.current_location_id)
        memories = self.storage_manager.get_memories(
            character_actions, player.character
        )
        memories_string = self.format_memories(memories)
        title, content, importance, location_description, status_description = (
            self.chain.invoke(
                {
                    "location_description": current_location.get_full_description(),
                    "character_description": player.character.get_description(),
                    "character_actions": character_actions,
                    "character_memories": memories_string,
                    "character_situation": player.current_status or "",
                }
            )
        )
        print("New player status", status_description)
        player.current_status = status_description or player.current_status
        self.storage_manager.add_observation(
            title, content, importance, player.character
        )
        print("New location description", location_description)
        if location_description:
            interior_description = current_location.interior or ""
            current_location.interior = (
                interior_description + f"\n {location_description}"
            )
            self.storage_manager.save_map()


class ExplorationManager:
    def __init__(
        self,
        storage_manager: StorageManager,
        llm_model: BaseChatModel,
        settings: Settings,
    ):
        self.settings = settings
        self.storage_manager = storage_manager
        self.interior_generator = InteriorGenerator(llm_model)
        self.exploration_agent = ExplorationAgent(storage_manager, llm_model, settings)

    def generate_interior(self, location: Location) -> Location:
        return self.interior_generator.generate(location)

    def run(self):
        player = self.storage_manager.character_storage.player_characters[
            self.settings.main_player_id
        ]
        current_location = self.storage_manager.get_location(player.current_location_id)
        print("Current location:", current_location.name)
        if current_location.interior is None:
            current_location = self.generate_interior(current_location)
            print("Generated interior: ")
            print(current_location.interior)
            self.storage_manager.save_map()

        character_actions = "I decide to abandon the smell investigation and I go find more people here."
        self.exploration_agent.run(character_actions)


class ExplorationRouter:

    pass
