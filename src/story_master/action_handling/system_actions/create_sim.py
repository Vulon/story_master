from story_master.action_handling.action import Action

from langchain_core.language_models.chat_models import BaseChatModel

from story_master.action_handling.parameter import Parameter
from story_master.entities.handlers.event_handler import EventHandler
from story_master.entities.inventory import Inventory
from story_master.entities.location import Position
from story_master.entities.memory import Memory
from story_master.log import logger
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.entities.handlers.observation_handler import ObservationHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.generators.character_generation.character_generator import (
    CharacterGenerator,
)
from story_master.generators.character_generation.description_generator import (
    CharacterDescriptionGenerator,
)
from story_master.entities.sim import Sim
from story_master.entities.event import Event, SimReference, EventType

DEFAULT_REGION = 0


class SpawnSimAction(Action):
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
        self.character_generator = CharacterGenerator(
            llm_model, storage_handler, summary_handler
        )
        self.character_description_generator = CharacterDescriptionGenerator(llm_model)

    def execute(
        self,
        **kwargs,
    ):
        region = self.storage_handler.get_location(DEFAULT_REGION)
        location_description = region.get_description()
        character_description = self.character_description_generator.generate(
            "Create a new settler, that has just arrived in this region.",
            location_description,
        )
        character = self.character_generator.generate(
            character_description,
        )
        sim_id = self.storage_handler.character_storage.get_new_id()
        position = Position(location_id=DEFAULT_REGION, x=0, y=0)
        inventory = Inventory()
        memory = Memory()
        sim = Sim(
            id=sim_id,
            character=character,
            position=position,
            inventory=inventory,
            memory=memory,
            current_status="Just arrived in this region. Decided to settle here.",
        )
        logger.info(f"Created new character: {character}")
        self.storage_handler.character_storage.npc_characters[sim_id] = sim
        event = Event(
            type=EventType.SIM_SPAWN,
            description="A new settler has arrived in this region.",
            source=SimReference(sim_id=sim_id),
            position=position,
            radius=8,
            timestamp=self.storage_handler.game_storage.current_time,
        )
        self.event_handler.broadcast_event(event)

    def get_description(self) -> str:
        return "Create a new character in the simulation"

    def get_parameters(self) -> dict[str, Parameter]:
        return {}
