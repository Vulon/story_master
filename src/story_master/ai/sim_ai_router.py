from langchain_core.language_models.chat_models import BaseChatModel
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from story_master.log import logger
from story_master.entities.handlers.event_handler import EventHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.entities.handlers.observation_handler import ObservationHandler
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.action_handling.sim_actions.action_factory import ActionType
import re
from difflib import get_close_matches


SIM_ACTIONS = [ActionType.SPEAK]


class SimAiRouter:
    PROMPT = """
    You are an agentic router. 
    
    -Goal-
    Find the right action that the character should take. 
    
    -Steps-
    1. Analyze character's plan. 
    2. Analyze the list of actions available.
    3. Pick the right action.
        Choose the action that is most suitable for the character's plan.
        Write the name of the action directly.
    4. Output the action name in XML format
    
    -Plan-
    {plan}
    
    -Available actions-
    {actions}
    
    -Output format-
    <Action>Action</Action>
    
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
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output
        self.output_pattern = re.compile(r"<Action>(.*?)</Action>")

        self.action_names = [str(action) for action in SIM_ACTIONS]

    def parse_output(self, output: str) -> ActionType:
        try:
            output = output.replace("\n", " ").strip()
            match = self.output_pattern.search(output)
            raw_action_name = match.group(1)
            action_name = get_close_matches(raw_action_name, self.action_names)[0]
            return ActionType(action_name)
        except Exception as e:
            logger.error(f"SimAiRouter. Failed to parse output: {output}")
            raise e

    def route(self, plan: str) -> ActionType:
        actions = "\n".join(self.action_names)
        action = self.chain.invoke({"plan": plan, "actions": actions})
        return action
