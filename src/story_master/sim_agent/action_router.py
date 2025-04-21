from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from story_master.sim_agent.tools import get_nearby_characters
from story_master.sim_agent.actions import speak_action


class ActionRouter:
    PROMPT = """
You are a routing agent in a simulation game.
You job is to decide, what action the character should take.

---

- Goal -
Decide, what action should the character choose.
Or pick a function, that will provide required information to decide what action to take.

---

- Details - 
You have 2 types of tools available to you. 
Retrieval functions are used to gather more context. Use them, when you can't confidently choose an action and fill all required parameters for that action.
The second type of tools is action. The action decides, what the character will do next. Picking an action ends this agentic loop. 
The action might require parameters. Please, think carefully, what parameters to set. You might need to retrieve more context to get all parameters. 
You should output only one tool call. You can also provide your reasoning.
---

- Input -
You will receive the list of messages, that the agent has collected during this workflow. 
It can contain agent decisions, tool calls and other information.


Output:
    """

    def __init__(self, llm_client: BaseChatModel):
        available_tools = [get_nearby_characters, speak_action]
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
