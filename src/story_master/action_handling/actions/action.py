from abc import abstractmethod, ABC

from langchain_core.language_models.chat_models import BaseChatModel

from story_master.storage.storage_manager import StorageManager
from story_master.storage.summary import SummaryAgent
from story_master.action_handling.parameter import Parameter


class Action(ABC):
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
    def execute(self, **kwargs):
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_parameters(self) -> dict[str, Parameter]:
        pass
