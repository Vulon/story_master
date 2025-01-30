from story_master.action_handling.actions.action import Action
from story_master.action_handling.actions.character.create_character_action import (
    CreateCharacterAction,
)
from story_master.storage.storage_manager import StorageManager
from story_master.storage.summary import SummaryAgent
from langchain_core.language_models.chat_models import BaseChatModel
from enum import StrEnum
from story_master.action_handling.actions.character.dialog_action import DialogAction


class ActionType(StrEnum):
    CREATE_CHARACTER = "create_character"
    DIALOG = "dialog"


def create_action_table(
    llm_model: BaseChatModel,
    summary_agent: SummaryAgent,
    storage_manager: StorageManager,
) -> dict[ActionType, Action]:
    return {
        ActionType.CREATE_CHARACTER: CreateCharacterAction(
            llm_model, summary_agent, storage_manager
        ),
        ActionType.DIALOG: DialogAction(llm_model, summary_agent, storage_manager),
    }
