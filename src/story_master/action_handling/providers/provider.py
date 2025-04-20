from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel

from story_master.entities.handlers.event_handler import EventHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.action_handling.parameter import Parameter, FilledParameter


class Provider(ABC):
    def __init__(
        self,
        llm_model: BaseChatModel,
        summary_handler: SummaryHandler,
        storage_handler: StorageHandler,
        memory_handler: MemoryHandler,
        event_handler: EventHandler,
    ):
        self.llm_model = llm_model
        self.summary_handler = summary_handler
        self.storage_handler = storage_handler
        self.memory_handler = memory_handler
        self.event_handler = event_handler

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_input_parameters(self) -> dict[str, Parameter]:
        pass

    @abstractmethod
    def get_output_parameters(self) -> dict[str, Parameter]:
        pass

    @abstractmethod
    def execute(
        self, target_parameter: Parameter, **kwargs
    ) -> dict[str, FilledParameter]:
        pass
