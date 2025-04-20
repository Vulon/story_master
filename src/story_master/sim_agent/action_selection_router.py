from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from story_master.sim_agent.tools import get_nearby_characters
from pydantic import BaseModel


class select_action(BaseModel):
    """
    By calling this function, the agent shows, that the provided information is enough to select action.
    This function moves the agent to the next phase.
    """


class ActionSelectionRouter:
    PROMPT = """
You are a routing agent in a simulation game. Your job is to decide the next step in the character's reasoning process.

---

- Goal -
Decide whether the character is ready to choose an action, or if more information is needed before doing so.

---

- Details - 
You need to pick a tool function that should be called next. You have to choose one function. 
The functions are mostly used to provide further information to the agent. This information will be later used by the agent. 
The function "select_action" is a way for you to show, that the agent already has enough information to decide the next action for the character. 

---

- Input -
You will receive the list of messages, that the agent has collected during this workflow. 
It can contain agent decisions, tool calls and other information.


Output:
    """

    def __init__(self, llm_client: BaseChatModel):
        available_tools = [get_nearby_characters, select_action]
        self.bound_llm = llm_client.bind_tools(available_tools, tool_choice="any")

        prompt_template = ChatPromptTemplate(
            [("system", self.PROMPT), MessagesPlaceholder("messages")]
        )
        self.chain = (
            prompt_template | self.bound_llm
        )  # | PydanticToolsParser(tools=available_tools)

    def run(self, messages: list) -> AIMessage:
        ai_message: AIMessage = self.chain.invoke({"messages": messages})
        return ai_message
