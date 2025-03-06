from langchain_core.language_models.chat_models import BaseChatModel

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


class PlanGenerator:
    PROMPT = """    
    You are an agent for a simulation game. 
    Role-play as a character and generate a plan of actions for the character.
    
    -Goal-
    Generate a plan of actions.
    
    -Steps-
    1. Analyze the recent events.
    2. Analyze your previous plan, if any.
    
    
    
    """

    def __init__(
        self,
        llm_model: BaseChatModel,
    ):
        pass
