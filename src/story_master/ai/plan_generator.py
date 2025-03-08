from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from story_master.entities.handlers.event_handler import EventHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.entities.handlers.observation_handler import ObservationHandler
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.ai.sim_ai_router import ACTION_DESCRIPTIONS
import json


class PlanGenerator:
    PROMPT = """    
    You are an agent for a simulation game. 
    Role-play as a character in this game. 
    
    -Goal-
    Decide what the character should do next, based on available options.
    
    -Steps-
    1. Analyze recent events.
    2. Analyze previous plan if any.
    3. Analyze actions, that can be performed by the character.
        Focus your plan on available actions.
    4. Generate a short plan based on provided actions for the character.
        It should describe short-term goal, that the character will try to achieve.
        Write the plan as if the character is thinking about it.
    
    -Events-
    {events}
    
    -Previous plan-
    {previous_plan}
    
    -Available actions-    
    {actions}
    
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
        self.llm_model = llm_model
        self.summary_handler = summary_handler
        self.storage_handler = storage_handler
        self.observation_handler = observation_handler
        self.memory_handler = memory_handler
        self.event_handler = event_handler

        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser()

    def generate(self, events: list[str], previous_plan: str) -> str:
        actions = json.dumps(ACTION_DESCRIPTIONS)
        plan = self.chain.invoke(
            {"events": events, "previous_plan": previous_plan, "actions": actions}
        )

        return plan


"""
Create plan iteratively. 
Need to analyze:
 recent events
 previous plan
 memories
 characters nearby
 objects
 location
 self description
 status
Use a list of available actions to generate a plan. 

"""
