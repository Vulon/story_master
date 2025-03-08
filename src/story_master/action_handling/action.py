from abc import abstractmethod, ABC

from langchain_core.language_models.chat_models import BaseChatModel

from story_master.entities.handlers.event_handler import EventHandler
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.entities.handlers.observation_handler import ObservationHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.action_handling.parameter import Parameter


class Action(ABC):
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
        self.observation_handler = observation_handler
        self.memory_handler = memory_handler
        self.event_handler = event_handler

    @abstractmethod
    def execute(self, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def get_description() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_parameters() -> dict[str, Parameter]:
        pass
