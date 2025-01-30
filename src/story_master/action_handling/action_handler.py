from langchain_core.language_models.chat_models import BaseChatModel

from story_master.storage.storage_manager import StorageManager
from story_master.storage.summary import SummaryAgent
from story_master.action_handling.parameter import FilledParameter

from story_master.action_handling.actions.action_factory import (
    create_action_table,
    ActionType,
)
from story_master.action_handling.context_manager import ContextManager
from story_master.action_handling.providers.provider_factory import create_provider_list


class ActionHandler:
    def __init__(
        self,
        llm_model: BaseChatModel,
        summary_agent: SummaryAgent,
        storage_manager: StorageManager,
    ):
        self.llm_model = llm_model
        self.summary_agent = summary_agent
        self.storage_manager = storage_manager

        self.action_table = create_action_table(
            llm_model, summary_agent, storage_manager
        )
        providers_list = create_provider_list(llm_model, summary_agent, storage_manager)
        self.context_manager = ContextManager(providers_list)

    def handle(
        self, action_type: ActionType, intent: str, character_id: int | None = None
    ):
        action = self.action_table[action_type]
        self.context_manager.clear()
        self.context_manager.add(
            FilledParameter(
                name="intent", value=intent, description="Intent for the action"
            )
        )
        if character_id is not None:
            self.context_manager.add(
                FilledParameter(
                    name="actor_character_id",
                    value=character_id,
                    description="ID of the character associated with the action",
                )
            )
        filled_parameters = {
            parameter_name: self.context_manager.get(parameter_name).value
            for parameter_name in action.get_parameters().keys()
        }
        action.execute(**filled_parameters)
