from langchain_core.language_models.chat_models import BaseChatModel

from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.action_handling.providers.provider import Provider
# from story_master.action_handling.providers.location_id import LocationProvider
# from story_master.action_handling.providers.new_character_description import (
#     CharacterDescriptionProvider,
# )
# from story_master.action_handling.providers.responder_character_id import (
#     ResponderCharacterProvider,
# )
# from story_master.action_handling.providers.target_object_id import TargetObjectProvider


def create_provider_list(
    llm_model: BaseChatModel,
        summary_handler: SummaryHandler,
        storage_handler: StorageHandler
) -> list[Provider]:
    return [
        # LocationProvider(llm_model, summary_handler, storage_handler),
        # CharacterDescriptionProvider(llm_model, summary_handler, storage_handler),
        # ResponderCharacterProvider(llm_model, summary_handler, storage_handler),
        # TargetObjectProvider(llm_model, summary_handler, storage_handler),
    ]
