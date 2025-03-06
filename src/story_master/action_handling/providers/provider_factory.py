from langchain_core.language_models.chat_models import BaseChatModel

from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.action_handling.providers.provider import Provider
from story_master.action_handling.providers.target_character_provider import (
    TargetCharacterProvider,
)
from story_master.action_handling.providers.speech_provider import SpeechProvider
from story_master.entities.handlers.observation_handler import ObservationHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.entities.handlers.event_handler import EventHandler


def create_provider_list(
    llm_model: BaseChatModel,
    summary_handler: SummaryHandler,
    storage_handler: StorageHandler,
    observation_handler: ObservationHandler,
    memory_handler: MemoryHandler,
    event_handler: EventHandler,
) -> list[Provider]:
    return [
        TargetCharacterProvider(
            llm_model,
            summary_handler,
            storage_handler,
            observation_handler,
            memory_handler,
            event_handler,
        ),
        SpeechProvider(
            llm_model,
            summary_handler,
            storage_handler,
            observation_handler,
            memory_handler,
            event_handler,
        ),
    ]
