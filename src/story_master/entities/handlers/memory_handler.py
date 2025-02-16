from langchain_community.utils.math import cosine_similarity
from langchain_core.embeddings import Embeddings
from story_master.settings import Settings
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.sim import Sim
from story_master.entities.memory import Observation
import numpy as np
import math


class MemoryHandler:
    def __init__(
        self,
        settings: Settings,
        embeddings_client: Embeddings,
        storage_handler: StorageHandler,
    ):
        self.settings = settings
        self.embeddings_client = embeddings_client
        self.storage_handler = storage_handler

    def add_observation(
        self, title: str, content: str, importance: int, sim: Sim
    ) -> None:
        embeddings = self.embeddings_client.embed_query(content)

        memory_ids = [memory.id for memory in sim.memory.personal_memories]
        max_id = max(memory_ids) + 1 if memory_ids else 0
        timestamp = self.storage_handler.game_storage.current_time
        memory = Observation(
            id=max_id,
            timestamp=timestamp,
            title=title,
            content=content,
            importance=importance,
            embeddings=embeddings,
        )
        sim.memory.personal_memories.append(memory)

    def get_memories(
        self, query: str, sim: Sim, max_similar_memories: int = 5
    ) -> list[Observation]:
        query_embeddings = self.embeddings_client.embed_query(query)
        query_embeddings = np.array(query_embeddings).reshape(1, -1)
        current_time = self.storage_handler.game_storage.current_time
        scored_memories = []
        for memory in sim.memory.personal_memories:
            memory_embeddings = np.array(memory.embeddings).reshape(1, -1)
            distance = cosine_similarity(query_embeddings, memory_embeddings)
            time_difference = current_time - memory.timestamp
            importance = memory.importance
            score = (
                distance
                * importance
                / max(math.log(time_difference.total_seconds() / 60 + 1), 1)
            )
            scored_memories.append((memory, score))
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        return [memory for memory, _ in scored_memories[:max_similar_memories]]
