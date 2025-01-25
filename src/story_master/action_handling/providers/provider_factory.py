from langchain_core.language_models.chat_models import BaseChatModel

from story_master.storage.storage_manager import StorageManager
from story_master.storage.summary import SummaryAgent
from story_master.action_handling.providers.provider import Provider


def create_provider_list(
    llm_model: BaseChatModel,
    summary_agent: SummaryAgent,
    storage_manager: StorageManager,
) -> list[Provider]:
    pass
