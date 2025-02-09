import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from story_master.log import logger
from story_master.entities.location import Region, Object, Position, DEFAULT_WORLD_WIDTH, DEFAULT_WORLD_HEIGHT
from story_master.entities.handlers.summary_handler import SummaryHandler
from story_master.entities.handlers.storage_handler import StorageHandler

from story_master.generators.environment_generation.decomposer import MapDecomposer

class MapCreator:
    def __init__(self,
                 llm_model: BaseChatModel,
                 storage_handler: StorageHandler,
                summary_handler: SummaryHandler,
                 ):
        self.llm_model = llm_model
        self.storage_manager = storage_handler
        self.summary_handler = summary_handler

        self.map_decomposer = MapDecomposer(llm_model)

    def create_map(self) -> None:
        logger.info("Creating map")
        raw_regions = self.map_decomposer.generate()
        for raw_region in raw_regions:
            region_id = 0
            if location_ids := self.storage_manager.map.locations.keys():
                region_id = max(location_ids) + 1
            position = Position(
                x=raw_region.x,
                y=raw_region.y,
                location_id=None
            )
            region = Region(
                id=region_id,
                name=raw_region.name,
                description=raw_region.description,
                position=position,
            )
            self.storage_manager.map.locations[region_id] = region

        self.storage_manager.save_map()