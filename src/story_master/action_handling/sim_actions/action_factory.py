from story_master.action_handling.action import Action
from story_master.action_handling.sim_actions.character.speak import SpeakAction
from story_master.action_handling.system_actions.create_sim import SpawnSimAction
from story_master.entities.handlers.event_handler import EventHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from langchain_core.language_models.chat_models import BaseChatModel

from enum import StrEnum


class ActionType(StrEnum):
    SPAWN_SIM = "spawn_sim"
    SPEAK = "speak"


ACTION_CLASS_TABLE = {
    ActionType.SPAWN_SIM: SpawnSimAction,
    ActionType.SPEAK: SpeakAction,
}


def create_action_table(
    llm_model: BaseChatModel,
    summary_handler: SummaryHandler,
    storage_handler: StorageHandler,
    memory_handler: MemoryHandler,
    event_handler: EventHandler,
) -> dict[ActionType, Action]:
    return {
        action_type: action_class(
            llm_model,
            summary_handler,
            storage_handler,
            memory_handler,
            event_handler,
        )
        for action_type, action_class in ACTION_CLASS_TABLE.items()
    }
