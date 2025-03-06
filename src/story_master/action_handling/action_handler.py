from langchain_core.language_models.chat_models import BaseChatModel


from story_master.action_handling.parameter import FilledParameter

from story_master.action_handling.sim_actions.action_factory import (
    create_action_table,
    ActionType,
)
from story_master.action_handling.context_manager import ContextManager
from story_master.action_handling.providers.provider_factory import create_provider_list
from story_master.entities.handlers.event_handler import EventHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.entities.handlers.observation_handler import ObservationHandler
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler


class ActionHandler:
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

        self.action_table = create_action_table(
            llm_model,
            summary_handler,
            storage_handler,
            observation_handler,
            memory_handler,
            event_handler,
        )
        providers_list = create_provider_list(
            llm_model, summary_handler, storage_handler
        )
        self.context_manager = ContextManager(providers_list)

    def handle_sim_action(
        self, action_type: ActionType, parameters: list[FilledParameter]
    ):
        action = self.action_table[action_type]
        self.context_manager.clear()
        for parameter in parameters:
            self.context_manager.add(parameter)

        filled_parameters = {
            parameter_name: self.context_manager.get(parameter).value
            for parameter_name, parameter in action.get_parameters().items()
            if parameter.required
            or (
                not parameter.required
                and self.context_manager.is_parameter_filled(parameter_name)
            )
        }
        action.execute(**filled_parameters)

    def handle_system_action(
        self,
        action_type: ActionType,
    ):
        action = self.action_table[action_type]
        self.context_manager.clear()

        filled_parameters = {
            parameter_name: self.context_manager.get(parameter).value
            for parameter_name, parameter in action.get_parameters().items()
        }
        action.execute(**filled_parameters)
