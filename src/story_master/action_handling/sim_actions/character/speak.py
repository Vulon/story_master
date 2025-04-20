from story_master.action_handling.action import Action

from langchain_core.language_models.chat_models import BaseChatModel

from story_master.action_handling.parameter import Parameter
from story_master.entities.handlers.event_handler import EventHandler
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.entities.event import Event, SimReference, EventType


class SpeakAction(Action):
    def __init__(
        self,
        llm_model: BaseChatModel,
        summary_handler: SummaryHandler,
        storage_handler: StorageHandler,
        memory_handler: MemoryHandler,
        event_handler: EventHandler,
    ):
        super().__init__(
            llm_model,
            summary_handler,
            storage_handler,
            memory_handler,
            event_handler,
        )

    def execute(
        self,
        speech: str,
        actor_character_id: int,
        target_character_id: int | None = None,
        **kwargs,
    ):
        actor = self.storage_handler.get_sim(actor_character_id)
        target = None
        if target_character_id is not None:
            target = SimReference(sim_id=target_character_id)

        event = Event(
            type=EventType.SPEECH,
            description=speech,
            position=actor.position,
            radius=3,
            source=SimReference(sim_id=actor_character_id),
            target=target,
            timestamp=self.storage_handler.game_storage.current_time,
        )
        self.event_handler.broadcast_event(event)

    @staticmethod
    def get_description() -> str:
        return "Generate a speech for a character"

    @staticmethod
    def get_parameters() -> dict[str, Parameter]:
        return {
            "speech": Parameter(
                description="The speech to be spoken by the character",
                name="speech",
            ),
            "actor_character_id": Parameter(
                description="The ID of the character who is speaking",
                name="actor_character_id",
            ),
            "target_character_id": Parameter(
                description="The character who is being spoken to",
                name="target_character_id",
                required=False,
            ),
        }
