from langchain_core.messages import BaseMessage, ToolMessage
from typing_extensions import TypedDict
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph, START, END
from story_master.sim_agent.actions import ANY_ACTION_TYPE, ALL_ACTIONS
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.sim_agent.tools import WorldRetriever
from story_master.sim_agent.action_router import ActionRouter
from story_master.sim_agent.planning_router import (
    PlanningRouter,
)
from langchain.output_parsers import PydanticToolsParser


class SimActionState(TypedDict):
    messages: list[BaseMessage]
    phase: int
    sim_id: int
    selected_action: ANY_ACTION_TYPE | None


class SimActionGraph:
    def __init__(
        self, sim_id: int, llm_client: BaseChatModel, storage_handler: StorageHandler
    ):
        self.sim_id = sim_id
        self.base_client = llm_client
        self.storage_handler = storage_handler

        self.planning_router = PlanningRouter(llm_client)
        self.action_router = ActionRouter(llm_client)
        self.world_retriever = WorldRetriever(storage_handler)

    def _init_values_node(self, state: SimActionState) -> SimActionState:
        return SimActionState(
            messages=[],
            phase=1,
            sim_id=self.sim_id,
            selected_action=None,
        )

    def _planning_node(self, state: SimActionState) -> SimActionState:
        print("_planning_node.")
        if state["phase"] == 2:
            return state

        print("Running planning router")
        ai_message = self.planning_router.run(state["messages"])
        state["messages"].append(ai_message)

        while len(state["messages"][-1].tool_calls) == 0:
            print("Running planning router again")
            ai_message = self.planning_router.run(state["messages"])
            state["messages"].append(ai_message)
        last_message = state["messages"][-1]
        tool_name = last_message.tool_calls[0]["name"]
        if "select_action" == tool_name:
            state["phase"] = 2
        return state

    def _planning_router(self, state: SimActionState) -> str:
        print("_planning_router")
        if state["phase"] == 2:
            return "_action_node"

        last_message = state["messages"][-1]
        tool_name = last_message.tool_calls[0]["name"]
        print("Planning router tool name", tool_name)
        if "select_action" == tool_name:
            return "_action_node"
        return tool_name

    def _get_nearby_characters_node(self, state: SimActionState) -> SimActionState:
        print("_get_nearby_characters_node.")
        first_tool = state["messages"][-1].tool_calls[0]
        text = self.world_retriever.get_nearby_characters(state["sim_id"])
        message = ToolMessage(
            content=text, name=first_tool["name"], tool_call_id=first_tool["id"]
        )
        state["messages"].append(message)
        return state

    def _action_node(self, state: SimActionState) -> SimActionState:
        print("_action_node")
        ai_message = self.action_router.run(state["messages"])
        state["messages"].append(ai_message)
        while len(state["messages"][-1].tool_calls) == 0:
            print("Running action router again")
            ai_message = self.action_router.run(state["messages"])
            state["messages"].append(ai_message)
        last_message = state["messages"][-1]
        tool_name = last_message.tool_calls[0]["name"]
        if "action" in tool_name:
            parser = PydanticToolsParser(tools=ALL_ACTIONS)
            parsed_action = parser.invoke(last_message)
            state["selected_action"] = parsed_action
            print("Parsed action", parsed_action)
        return state

    def _action_router(self, state: SimActionState):
        print("_action_router")
        last_message = state["messages"][-1]
        tool_name = last_message.tool_calls[0]["name"]
        print("Second router tool name", tool_name)
        if "action" in tool_name:
            return END
        return tool_name

    def compile(self):
        graph_builder = StateGraph(SimActionState)
        graph_builder.add_node("init", self._init_values_node)
        graph_builder.add_node("_planning_node", self._planning_node)
        graph_builder.add_node("_action_node", self._action_node)
        graph_builder.add_node(
            "get_nearby_characters", self._get_nearby_characters_node
        )

        graph_builder.add_edge(START, "init")
        graph_builder.add_edge("init", "_planning_node")
        graph_builder.add_conditional_edges(
            "_planning_node",
            self._planning_router,
        )
        graph_builder.add_conditional_edges(
            "_action_node",
            self._action_router,
        )
        graph_builder.add_edge("get_nearby_characters", "_planning_node")
        return graph_builder.compile()
