import re
from difflib import get_close_matches
from enum import StrEnum

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser


from story_master.settings import Settings
from story_master.storage.storage_manager import StorageManager
from story_master.storage.storage_models import (
    Sim,
)


class ExplorationScenario(StrEnum):
    LOOK_AROUND = "Look around"
    DIALOG = "Dialog"
    RESOURCE_GATHERING = "Resource gathering"


class ExplorationRouter:
    PROMPT = """
    You are a router agent for Dungeons and Dragons game.

    -Goal-
    Identify the route that best handles the character's intent.

    -Steps-
     1. Read the character's intent.
     2. Read the description of the location.
     3. Read character's description
     4. Read character's memories
     5. Read the list of characters already present in the location.
     6. Identify the right route to handle the character's intent.
        Pick a single route from the list of available routes.        
        Try to find the closest one.
     7. Output the route you selected in XML format.        
        Format: <Route>Route name</Route>

    -Character intent-
    {character_intent}

    -Location description-
    {location_description}

    -Character description-
    {character_description}

    -Character memories-
    {character_memories}

    -Characters already present-
    {existing_characters}
    
    -List of routes-
    1. "Look around" - character wants to see what is happening around them. This is a general route that will provide a description of the location.
        "Look around" route will also generate a memory entry for the character and describe the characters already present in the location.        
    2. "Dialog" - character wants to speak with another character. This route will handle character's speech, generate a response and create a memory entry for the character.        
    3. "Resource gathering" - character wants to gather some resources. It can be anything from food, crafting materials, ores, etc.
        This route will change character's status and make him busy for a certain amount of time.
        
    -Output example-
    <Route>Look around</Route>
    or
    <Route>Dialog</Route>
    or
    <Route>Resource gathering</Route>

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
        self.pattern = re.compile(r"<Route>(.*?)</Route>")
        self.possible_intents = [
            str(ExplorationScenario.DIALOG),
            str(ExplorationScenario.LOOK_AROUND),
            str(ExplorationScenario.RESOURCE_GATHERING),
        ]
        self.chain = self.prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> ExplorationScenario:
        print("Raw exploration scenario output", output)
        output = output.replace("\n", " ")
        match = self.pattern.search(output)
        raw_scenario = match.group(1).lower().capitalize()
        scenario = get_close_matches(raw_scenario, self.possible_intents)[0]
        return ExplorationScenario(scenario)

    def format_location_sims(self, sims: list[Sim]) -> str:
        strings = []
        for sim in sims:
            strings.append(
                f"{sim.character.name} the {sim.character.type}. Current status: {sim.current_status}"
            )
        return " ; ".join(strings)

    def run(
        self,
        sim: Sim,
        intent: str,
        location_description: str,
        memories_description: str,
        character_description: str,
    ) -> ExplorationScenario:
        location = self.storage_manager.get_location(sim.current_location_id)
        location_sims = self.storage_manager.get_location_characters(location)
        scenario = self.chain.invoke(
            {
                "character_intent": intent,
                "location_description": location_description,
                "character_description": character_description,
                "character_memories": memories_description,
                "existing_characters": self.format_location_sims(location_sims),
            }
        )

        return scenario
