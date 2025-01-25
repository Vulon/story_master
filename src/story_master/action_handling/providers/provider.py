from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel

from story_master.storage.storage_manager import StorageManager
from story_master.storage.summary import SummaryAgent
from story_master.action_handling.parameter import Parameter


class Provider(ABC):
    def __init__(
        self,
        llm_model: BaseChatModel,
        summary_agent: SummaryAgent,
        storage_manager: StorageManager,
    ):
        self.llm_model = llm_model
        self.storage_manager = storage_manager
        self.summary_agent = summary_agent

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
    def execute(self, **kwargs):
        pass
