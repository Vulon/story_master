from story_master.action_handling.action import Action

from langchain_core.language_models.chat_models import BaseChatModel

from story_master.action_handling.parameter import Parameter
from story_master.entities.handlers.event_handler import EventHandler
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.entities.handlers.observation_handler import ObservationHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.entities.event import Event, SimReference, EventType

OBSERVATION_RADIUS = 5


class ObserveAction(Action):
    def __init__(
        self,
        llm_model: BaseChatModel,
        summary_handler: SummaryHandler,
        storage_handler: StorageHandler,
        observation_handler: ObservationHandler,
        memory_handler: MemoryHandler,
        event_handler: EventHandler,
    ):
        super().__init__(
            llm_model,
            summary_handler,
            storage_handler,
            observation_handler,
            memory_handler,
            event_handler,
        )

    def execute(
        self,
        actor_character_id: int,
        **kwargs,
    ):
        actor = self.storage_handler.get_sim(actor_character_id)
        sims = self.storage_handler.get_sims(actor.position, OBSERVATION_RADIUS)
        objects = self.storage_handler.get_objects(actor.position, OBSERVATION_RADIUS)
        sim_descriptions = []
        for sim in sims:
            sim_descriptions.append(self.memory_handler.get_sim_description(actor, sim))
        object_descriptions = []
        for obj in objects:
            object_descriptions.append(
                self.memory_handler.get_object_description(actor, obj)
            )
        text = "I observe the area around. "
        if len(sim_descriptions) > 0:
            text += "I see the following characters: <Characters>"
            text += ", ".join(sim_descriptions)
            text += "</Characters>. "
        else:
            text += "I see no characters nearby. "

        if len(object_descriptions) > 0:
            text += "I see the following objects: <Objects>"
            text += ", ".join(object_descriptions)
            text += "</Objects>. "
        else:
            text += "I see no objects nearby. "

        event = Event(
            type=EventType.OBSERVATION,
            description=text,
            position=actor.position,
            radius=0,
            source=SimReference(sim_id=actor_character_id),
            timestamp=self.storage_handler.game_storage.current_time,
        )
        self.event_handler.broadcast_event(event)

    @staticmethod
    def get_description() -> str:
        return "Describe objects and characters around the actor"

    @staticmethod
    def get_parameters() -> dict[str, Parameter]:
        return {
            "actor_character_id": Parameter(
                description="The ID of the character who is observing",
                name="actor_character_id",
            ),
        }
