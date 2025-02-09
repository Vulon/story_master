import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from story_master.log import logger
from story_master.storage.map.map_model import Region, Province, Settlement, Area, District, PointOfInterest, \
    LargeLocation, BaseLocation, LocationType
from story_master.generators.environment_generation.decomposer import RootDecomposer, RegionDecomposer, ProvinceDecomposer
from story_master.log import logger
from story_master.storage.storage_manager import Sim, StorageManager
from story_master.storage.summary import SummaryAgent

class MapCreator:
    def __init__(self,
                 llm_model: BaseChatModel,
                 summary_agent: SummaryAgent,
                 storage_manager: StorageManager,
                 ):
        self.llm_model = llm_model
        self.summary_agent = summary_agent
        self.storage_manager = storage_manager

        self.root_decomposer = RootDecomposer(llm_model)
        self.region_decomposer = RegionDecomposer(llm_model)
        self.province_decomposer = ProvinceDecomposer(llm_model)

    def create_map(self):
        logger.info("Creating map")
        regions = self.root_decomposer.generate()
        for name, description in regions:
            self.storage_manager.map.add_region(name, description)
        logger.info(f"Regions: {regions}")
        regions = [location for location in self.storage_manager.map.locations.values() if location.type == LocationType.REGION]

        for region in regions:
            logger.info(f"Decomposing region {region.name}")
            provinces = self.region_decomposer.generate(region)
            for name, description in provinces:
                self.storage_manager.map.add_province(name, description, region)
            logger.info(f"Provinces: {provinces}")
            logger.warn(f"Remove Debug limit")
            break

        provinces = [location for location in self.storage_manager.map.locations.values() if location.type == LocationType.PROVINCE]
        for province in provinces:
            region = self.storage_manager.get_location(province.parent_location)
            logger.info(f"Decomposing province {province.name}")
            settlements = self.province_decomposer.generate(province, [region, province])
            for name, description, settlement_flag in settlements:
                if settlement_flag:
                    self.storage_manager.map.add_settlement(name, description, province)
                else:
                    self.storage_manager.map.add_area(name, description, province)
            logger.info(f"Settlements: {settlements}")
