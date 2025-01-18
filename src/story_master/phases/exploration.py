import re
from difflib import get_close_matches
from enum import StrEnum

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.entities.items.items import ItemStack
from story_master.graphs.environment_generation.interior_generator import (
    InteriorGenerator,
)
from story_master.phases.actions.dialog import DialogAgent
from story_master.phases.actions.gather_resources import ResourceGatheringAgent
from story_master.settings import Settings
from story_master.storage.map.map_model import Location
from story_master.storage.memory.memory_model import Observation
from story_master.storage.storage_manager import StorageManager
from story_master.phases.actions.look_around import LookAroundAgent
from story_master.phases.actions.make_observation import ObservationAgent
from story_master.storage.storage_models import Sim, CharacterAction, ResourceGatheredEvent, GameEvent


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
            str(ExplorationScenario.DIALOG), str(ExplorationScenario.LOOK_AROUND),
            str(ExplorationScenario.RESOURCE_GATHERING)
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
            strings.append(f"{sim.character.name} the {sim.character.type}. Current status: {sim.current_status}")
        return " ; ".join(strings)

    def run(self, sim: Sim, intent: str) -> ExplorationScenario:
        location = self.storage_manager.get_location(sim.current_location_id)
        memories = self.storage_manager.get_memories(intent, sim)
        location_sims = self.storage_manager.get_location_characters(location)
        scenario = self.chain.invoke({
            "character_intent": intent,
            "location_description": location.get_full_description(),
            "character_description": sim.character.get_description(),
            "character_memories": self.storage_manager.format_memories(memories),
            "existing_characters": self.format_location_sims(location_sims),
        })
        print("Selected scenario:", scenario)
        return scenario

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
        self.look_around_agent = LookAroundAgent(llm_model, storage_manager)
        self.dialog_agent = DialogAgent(llm_model, storage_manager)
        self.observation_agent = ObservationAgent(storage_manager, llm_model, settings)
        self.resource_gathering_agent = ResourceGatheringAgent(llm_model, storage_manager)
        self.router = ExplorationRouter(storage_manager, llm_model, settings)

    def generate_interior(self, location: Location) -> Location:
        return self.interior_generator.generate(location)

    def handle_look_around(self, sim: Sim, intent: str) -> str:
        area_description = self.look_around_agent.run(sim, intent)
        print("Area description:", area_description)
        context = f"""{sim.character.name} is looking around and sees: {area_description}"""
        self.observation_agent.run(sim, context)
        return area_description

    def handle_dialog(self, sim: Sim, intent: str) -> str:
        response, responder = self.dialog_agent.run(sim, intent)
        question_context = f"""
        {sim.character.name} is saying "{intent}" to {responder.character.name}.
        {responder.character.name} replied: "{response}"
        """
        self.observation_agent.run(sim, question_context)
        self.observation_agent.run(responder, question_context)
        return response

    def handle_resource_gathering(self, sim: Sim, intent: str) -> str:
        resource, amount, time = self.resource_gathering_agent.run(sim, intent)
        finish_time = self.storage_manager.game_storage.current_time + time
        event = ResourceGatheredEvent(
            timestamp=finish_time,
            sim_id=sim.id,
            resource=resource,
            quantity=amount,
        )
        self.storage_manager.game_storage.events_queue.append(event)
        sim.is_busy = True
        sim.current_status = f"Gathering {resource.name} for {time} hours"
        return f"{sim.character.name} is gathering {amount} pounds of {resource.name} for {time} hours"


    def process_character_action(self, action: CharacterAction) -> str:
        sim = self.storage_manager.get_sim(action.sim_id)
        current_location = self.storage_manager.get_location(sim.current_location_id)
        print("Current location:", current_location.name)
        if current_location.interior is None:
            current_location = self.generate_interior(current_location)
            print("Generated interior: ")
            print(current_location.interior)
            self.storage_manager.save_map()
        scenario = self.router.run(sim, action.intent)
        print("Scenario: ", scenario)

        if scenario == ExplorationScenario.LOOK_AROUND:
            return self.handle_look_around(sim, action.intent)
        elif scenario == ExplorationScenario.DIALOG:
            return self.handle_dialog(sim, action.intent)
        elif scenario == ExplorationScenario.RESOURCE_GATHERING:
            return self.handle_resource_gathering(sim, action.intent)

    def process_gathering_event(self, event: ResourceGatheredEvent):
        sim = self.storage_manager.get_sim(event.sim_id)

        if (name := event.resource.name) in sim.character.items:
            sim.character.items[name].quantity += event.quantity
        else:
            sim.character.items[name] = ItemStack(item=event.resource, quantity=event.quantity)
        sim.is_busy = False
        sim.current_status = f"Finished gathering {event.resource.name}"
        context = f"""
        {sim.character.name} gathered {event.quantity} pounds of {event.resource.name}.        
        """
        self.observation_agent.run(sim, context)




# Gather resources
# Trade with another character
# Craft items
# Forage for food
# Interact with environment (Open chests, read books)
# Rest and recover
# Learn new skills
# Complete quests
# Investigate locations
# Perform skill checks
