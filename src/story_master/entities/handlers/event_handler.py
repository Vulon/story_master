from story_master.entities.event import Event
from story_master.entities.handlers.storage_handler import StorageHandler


class EventHandler:
    def __init__(
        self,
        storage_handler: StorageHandler,
    ):
        self.storage_handler = storage_handler

    def broadcast_event(self, event: Event) -> None:
        receivers = []
        for sim in self.storage_handler.character_storage.npc_characters.values():
            if event.position.is_close(sim.position, event.radius):
                receivers.append(sim)
        for sim in self.storage_handler.character_storage.player_characters.values():
            if event.position.is_close(sim.position, event.radius):
                receivers.append(sim)
        for sim in receivers:
            sim.events.append(event)
