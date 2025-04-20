from langchain_core.embeddings import Embeddings
from langchain_chroma import Chroma
from story_master.settings import StorageSettings
from story_master.entities.memory import MemoryTag
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.location import Position
import datetime


class MemoryHandler:
    def __init__(
        self,
        embeddings_client: Embeddings,
        storage_settings: StorageSettings,
        storage_handler: StorageHandler,
    ):
        self.memory_store = Chroma(
            collection_name=storage_settings.memory_collection,
            embedding_function=embeddings_client,
            persist_directory=str(storage_settings.data_file_path),
        )
        self.storage_handler = storage_handler

    def add_memory(
        self,
        memory_owner_id: int,
        content: str,
        tag: MemoryTag | None = None,
        importance: int = 5,
        related_entity_id: int | None = None,
        position: Position | None = None,
    ) -> None:
        position_json = position.model_dump_json() if position else ""
        current_datetime = (
            self.storage_handler.game_storage.current_time
            + datetime.timedelta(days=365 * 600)
        )

        metadata = {
            "memory_owner_id": memory_owner_id,
            "tag": tag,
            "importance": importance,
            "related_entity_id": related_entity_id,
            "position": position_json,
            "timestamp": current_datetime.timestamp(),
        }
        self.memory_store.add_texts([content], metadatas=[metadata])
