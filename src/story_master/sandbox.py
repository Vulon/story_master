from story_master.sim_agent.action_graph import SimActionGraph
from story_master.entities.handlers.storage_handler import StorageHandler
from story_master.llm_client import get_client

from story_master.settings import Settings

# engine = Engine()
# engine.run()

# generate_memories()


client = get_client()
settings = Settings()
storage_handler = StorageHandler(settings)
graph = SimActionGraph(0, client, storage_handler)
compiled_graph = graph.compile()
output = compiled_graph.invoke({})
print("Graph output", output)
