from story_master.settings import Settings
from gqlalchemy import Memgraph
from functools import lru_cache


@lru_cache
def get_db() -> Memgraph:
    settings = Settings()
    db = Memgraph(host=settings.db_settings.host, port=settings.db_settings.port)
    return db
