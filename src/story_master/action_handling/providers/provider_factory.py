from langchain_core.language_models.chat_models import BaseChatModel

from story_master.storage.storage_manager import StorageManager
from story_master.storage.summary import SummaryAgent
from story_master.action_handling.providers.provider import Provider
from story_master.action_handling.providers.location_id import LocationProvider
from story_master.action_handling.providers.new_character_description import (
    CharacterDescriptionProvider,
)
from story_master.action_handling.providers.responder_character_id import (
    ResponderCharacterProvider,
)
from story_master.action_handling.providers.target_object_id import TargetObjectProvider


def create_provider_list(
    llm_model: BaseChatModel,
    summary_agent: SummaryAgent,
    storage_manager: StorageManager,
) -> list[Provider]:
    return [
        LocationProvider(llm_model, summary_agent, storage_manager),
        CharacterDescriptionProvider(llm_model, summary_agent, storage_manager),
        ResponderCharacterProvider(llm_model, summary_agent, storage_manager),
        TargetObjectProvider(llm_model, summary_agent, storage_manager),
    ]
