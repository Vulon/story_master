from story_master.llm_client import get_embeddings_client
from story_master.settings import Settings
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.entities.handlers.memory_handler import MemoryHandler
from story_master.entities.memory import MemoryTag


def generate_memories():
    settings = Settings()
    embeddings_client = get_embeddings_client()

    storage_handler = StorageHandler(settings)

    memory_handler = MemoryHandler(embeddings_client, settings.storage, storage_handler)

    character_0_lines = [
        "I saw another settler nearby. I decided to greet them and ask where they come from.",
        "They said their name is Sigrun Frostwhisker. Strange name, but it suits her look.",
        "I asked if she’s alone or with others. The tundra is not kind to the solitary.",
        "She said she’s been surviving alone out here. Brave, or reckless?",
        "I offered to share my fire, at least for a night. It’s what we do out here.",
    ]
    character_1_lines = [
        "A stranger approached me and asked about my origins. I told them I come from the North plains.",
        "He introduced himself as Jormundur. He seems used to the cold.",
        "He seemed curious if I had companions. I told him I travel light, alone, as always.",
        "He nodded with understanding. Perhaps he knows what that’s like.",
        "She accepted the offer. We sat silently for a while, just the crackling of flame between us",
    ]

    for i in range(len(character_0_lines)):
        line_0 = character_0_lines[i]
        line_1 = character_1_lines[i]
        memory_handler.add_memory(
            0, line_0, MemoryTag.RELATIONSHIP, related_entity_id=1
        )
        memory_handler.add_memory(
            1, line_1, MemoryTag.RELATIONSHIP, related_entity_id=0
        )
