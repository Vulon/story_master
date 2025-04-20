from langchain_core.language_models.chat_models import BaseChatModel

from story_master.action_handling.parameter import FilledParameter
from story_master.ai.plan_generator import PlanGenerator
from story_master.entities.event import EventType, Event, SimReference
from story_master.entities.handlers.event_handler import EventHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.entities.sim import Sim
from story_master.log import logger
from story_master.action_handling.action_handler import ActionHandler
from story_master.ai.sim_ai_router import SimAiRouter

"""
Split the handling into phases.
1 - read events. Update memories. 
2 - Use parsed events to update plan
3 - Use plan to get an action from router. 
4 - Fill parameters for the selected action 


Use agentic RAG for plan creation. Use simple action handling for parsing parameters.
Add details about actions to the plan generator.  

"""


class SimAiHandler:
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

        self.action_handler = ActionHandler(
            llm_model,
            summary_handler,
            storage_handler,
            memory_handler,
            event_handler,
        )
        self.ai_router = SimAiRouter(
            llm_model,
            summary_handler,
            storage_handler,
            memory_handler,
            event_handler,
        )
        self.plan_generator = PlanGenerator(
            llm_model,
            summary_handler,
            storage_handler,
            memory_handler,
            event_handler,
        )

    def _handle_speech_event(self, sim: Sim, event: Event) -> str:
        source_sim = self.storage_handler.get_sim(event.source.sim_id)
        if source_sim.id == sim.id:
            description = f'I said: "{event.description}".'
        else:
            source_name = self.memory_handler.get_sim_name(sim, source_sim)
            if not source_name:
                source_name = self.memory_handler.get_sim_description(sim, source_sim)
            description = f'{source_name} said: "{event.description}".'

        if isinstance(event.target, SimReference):
            if event.target.sim_id == sim.id:
                description += " They said it to me."
            else:
                target_sim = self.storage_handler.get_sim(event.target.sim_id)
                target_name = self.memory_handler.get_sim_name(sim, target_sim)
                if not target_name:
                    target_name = self.memory_handler.get_sim_description(
                        sim, target_sim
                    )
                description += f" They were saying it to {target_name}."
        logger.info(f"Handling speech event. Description: {description}")
        if event.source.sim_id != sim.id:
            logger.info(f"Updating relationship between {sim.id} and {source_sim.id}")
            self.memory_handler.update_relationship(sim, source_sim, description)
        if event.target and event.target.sim_id != sim.id:
            logger.info(
                f"Updating relationship between {sim.id} and {event.target.sim_id}"
            )
            target_sim = self.storage_handler.get_sim(event.target.sim_id)
            self.memory_handler.update_relationship(sim, target_sim, description)

        self.observation_handler.run(sim, description)
        return description

    def _handle_spawn_event(self, sim: Sim, event: Event) -> str:
        source_sim = self.storage_handler.get_sim(event.source.sim_id)
        if source_sim.id == sim.id:
            description = "I arrived in this region."
        else:
            source_name = self.memory_handler.get_sim_name(sim, source_sim)
            if not source_name:
                source_name = self.memory_handler.get_sim_description(sim, source_sim)
            description = f'I notice, that a new settler arrived. Here is what I know about them: {source_name}".'
            self.memory_handler.update_relationship(sim, source_sim, description)

        location = self.storage_handler.get_location(source_sim.position.location_id)
        location_description = location.get_description()

        self.observation_handler.run(
            sim, description, location_description=location_description
        )
        return description

    def _handle_observation_event(self, sim: Sim, event: Event) -> str:
        description = event.description
        location = self.storage_handler.get_location(event.position.location_id)
        location_description = (
            f"{location.name}. Position: x:{event.position.x}, y:{event.position.y}."
        )
        self.observation_handler.run(
            sim, description, location_description=location_description
        )
        return description

    def handle_events(self, sim: Sim) -> list[str]:
        event_descriptions = []
        for event in sim.events:
            if event.type == EventType.SPEECH:
                event_descriptions.append(self._handle_speech_event(sim, event))
            elif event.type == EventType.SIM_SPAWN:
                event_descriptions.append(self._handle_spawn_event(sim, event))
            elif event.type == EventType.OBSERVATION:
                event_descriptions.append(self._handle_observation_event(sim, event))
            else:
                raise NotImplementedError()
        return event_descriptions

    def handle(self, sim_id: int):
        actor = self.storage_handler.get_sim(sim_id)
        event_descriptions = self.handle_events(actor)

        logger.info(f"Recent events: {event_descriptions}")
        plan = self.plan_generator.generate(event_descriptions, actor.memory.plan)
        logger.info(f"Generated plan: {plan}")
        actor.memory.plan = plan
        action_type = self.ai_router.route(plan)
        actor.events.clear()
        self.action_handler.handle_sim_action(
            action_type,
            [
                FilledParameter(
                    name="actor_character_id",
                    value=sim_id,
                    description="The id of the actor character",
                ),
                FilledParameter(
                    name="plan",
                    value=plan,
                    description="The plan of the actor character",
                ),
            ],
        )
