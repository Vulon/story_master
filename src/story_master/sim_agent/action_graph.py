from langchain_core.messages import BaseMessage, ToolMessage
from typing_extensions import TypedDict
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph, START, END

from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.sim_agent.tools import WorldRetriever
from story_master.sim_agent.action_router import ActionRouter
from story_master.sim_agent.planning_router import (
    PlanningRouter,
)


class SimActionState(TypedDict):
    messages: list[BaseMessage]
    phase: int
    sim_id: int
    new_tool_calls: list[dict]
    selected_action: dict


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
            new_tool_calls=[],
            selected_action={},
        )

    def _first_cycle_start_node(self, state: SimActionState) -> SimActionState:
        return state

    def _first_router(self, state: SimActionState) -> str:
        print(f"_first_router_node. state: {state}")
        if state["phase"] == 2:
            return "_second_cycle_start_node"

        while len(state["new_tool_calls"]) == 0:
            print("Running planning router")
            ai_message = self.planning_router.run(state["messages"])
            state["new_tool_calls"].extend(ai_message.tool_calls)
            state["messages"].append(ai_message)

        first_tool = state["new_tool_calls"][0]
        tool_name = first_tool["name"]
        print("First router tool name", tool_name)
        if "select_action" == tool_name:
            state["new_tool_calls"].pop(0)
            state["phase"] = 2
            return "_second_cycle_start_node"
        return tool_name

    def _get_nearby_characters_node(self, state: SimActionState) -> SimActionState:
        print(f"_get_nearby_characters_node. state: {state}")
        first_tool = state["new_tool_calls"].pop(0)
        text = self.world_retriever.get_nearby_characters(state["sim_id"])
        message = ToolMessage(
            content=text, name=first_tool["name"], tool_call_id=first_tool["id"]
        )
        state["messages"].append(message)
        return state

    def _second_cycle_start_node(self, state: SimActionState) -> SimActionState:
        print("Second cycle start node")
        return state

    def _second_router(self, state: SimActionState):
        while len(state["new_tool_calls"]) == 0:
            print("Running action router")
            ai_message = self.action_router.run(state["messages"])
            state["new_tool_calls"].extend(ai_message.tool_calls)
            state["messages"].append(ai_message)

        first_tool = state["new_tool_calls"][0]
        tool_name = first_tool["name"]
        print("Second router tool name", tool_name)
        if "action" in tool_name:
            state["selected_action"] = first_tool
            return END
        return tool_name

    def compile(self):
        graph_builder = StateGraph(SimActionState)
        graph_builder.add_node("init", self._init_values_node)
        graph_builder.add_node("_first_cycle_start_node", self._first_cycle_start_node)
        graph_builder.add_node(
            "_second_cycle_start_node", self._second_cycle_start_node
        )
        graph_builder.add_node(
            "get_nearby_characters", self._get_nearby_characters_node
        )

        graph_builder.add_edge(START, "init")
        graph_builder.add_edge("init", "_first_cycle_start_node")
        graph_builder.add_conditional_edges(
            "_first_cycle_start_node",
            self._first_router,
        )
        graph_builder.add_conditional_edges(
            "_second_cycle_start_node",
            self._second_router,
        )
        graph_builder.add_edge("get_nearby_characters", "_first_cycle_start_node")
        return graph_builder.compile()
