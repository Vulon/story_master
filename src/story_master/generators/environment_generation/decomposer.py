import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from story_master.log import logger
from story_master.storage.map.map_model import Region, Province, Settlement, Area, District, PointOfInterest, LargeLocation, BaseLocation

class BaseDecomposer:

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model


    def parse_output(self, output: str) -> list[tuple[str, str]]:
        pass

    def generate(self, parent_location: BaseLocation, location_tree_path: list[BaseLocation]) -> list[tuple[str, str]]:
        pass

class RootDecomposer(BaseDecomposer):
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Create regions, that the game world is divided into.
    
    -Steps-
    1. Think, how the world should be divided into regions.
        The world should be based on the Sword Coast setting.
        Regions should be large areas, like countries.
        Regions should have different climates, cultures, and landscapes.
        For the context: the game map is divided into regions. 
        Regions are divided into provinces, which are divided into settlements or areas.
        You need to only create regions.
        There must be at least 5 regions.
    2. Write a short description for every region, describing, what features it has.
        The description should be 3-4 sentences long.
    3. Output the regions in XML format.
        For every region output the name and description.
        Format: 
        <Region>
            <Name>Region name</Name>
            <Description>Region description</Description>
        </Region>
        
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        super().__init__(llm_model)
        self.region_pattern = re.compile(r"<Region>(.*?)</Region>")
        self.name_pattern = re.compile(r"<Name>(.*?)</Name>")
        self.description_pattern = re.compile(r"<Description>(.*?)</Description>")

        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[tuple[str, str]]:
        try:
            output = output.replace("\n", " ")
            regions = self.region_pattern.findall(output)
        except Exception as e:
            logger.error(f"RootDecomposer. Failed to parse output: {output}")
            raise e

        parsed_regions = []
        for region in regions:
            try:
                name = self.name_pattern.search(region).group(1)
                description = self.description_pattern.search(region).group(1)
                parsed_regions.append((name, description))
            except Exception:
                logger.error(f"RootDecomposer. Can't process region {region}")
                continue
        return parsed_regions

    def generate(self, *args) -> list[tuple[str, str]]:
        parsed_regions = self.chain.invoke(dict())
        return parsed_regions

class RegionDecomposer(BaseDecomposer):
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Create provinces, that the region is divided into.
    
    -Steps-
    1. Read the description of the region. 
    2. Think, how the region should be divided into provinces.
        Provinces are large areas, like states.
        Provinces can be different in climate, culture, and landscape, but they still should match the region.
        For the context: the game map is divided into regions. 
        Regions are divided into provinces, which are divided into settlements or areas.
        You need to only create provinces.
        There must be at least 3 provinces.
    3. Write a short description for every province, describing, what features it has.
        The description should be 3-4 sentences long.
    4. Output the provinces in XML format.
    
    -Region-
    {region_description}
    
    -Output format-
    <Province>
        <Name>Province name</Name>
        <Description>Province description</Description>
    </Province>   
    
    Output:    
    """

    def __init__(self, llm_model: BaseChatModel):
        super().__init__(llm_model)
        self.province_pattern = re.compile(r"<Province>(.*?)</Province>")
        self.name_pattern = re.compile(r"<Name>(.*?)</Name>")
        self.description_pattern = re.compile(r"<Description>(.*?)</Description>")

        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[tuple[str, str]]:
        try:
            output = output.replace("\n", " ")
            provinces = self.province_pattern.findall(output)
        except Exception as e:
            logger.error(f"RegionDecomposer. Failed to parse output: {output}")
            raise e

        parsed_provinces = []
        for province in provinces:
            try:
                name = self.name_pattern.search(province).group(1)
                description = self.description_pattern.search(province).group(1)
                parsed_provinces.append((name, description))
            except Exception:
                logger.error(f"RegionDecomposer. Can't process province {province}")
                continue
        return parsed_provinces

    def generate(self, parent_location: Region, *args) -> list[tuple[str, str]]:
        region_description = parent_location.get_description()

        parsed_provinces = self.chain.invoke({
            "region_description": region_description
        })
        return parsed_provinces

class ProvinceDecomposer(BaseDecomposer):
    PROMPT = """
    You are a Dungeons and Dragons agent.
    
    -Goal-
    Create settlements or areas, that the province is divided into.
    
    -Steps-
    1. Read the description of the region.
    2. Read the description of the province.
    3. Think, how the province should be divided into settlements or areas.
        Settlements are towns, villages, or cities.
        Areas are forests, mountains, or countryside.
        For the context: the game map is divided into regions. 
        Regions are divided into provinces, which are divided into settlements or areas.
        You need to only create settlements or areas.
        There must be at least 4 settlements or areas.
        You should figure the ration between settlements and areas based on the province description.
        Usually provinces have more areas than settlements.
    3. Write a short description for every settlement or area, describing, what features it has.
        The description should be 3-4 sentences long.
    4. For every location output the type: settlement or area.
    5. Output the settlements or areas in XML format.
    
    -Region-
    {region_description}
    
    -Province-
    {province_description}
    
    -Output format-
    <Settlement>
        <Name>Settlement name</Name>
        <Description>Settlement description</Description>
    </Settlement>
    <Area>
        <Name>Area name</Name>
        <Description>Area description</Description>
    </Area>   
    
    Output:    
    """

    def __init__(self, llm_model: BaseChatModel):
        super().__init__(llm_model)
        self.settlement_pattern = re.compile(r"<Settlement>(.*?)</Settlement>")
        self.area_pattern = re.compile(r"<Area>(.*?)</Area>")
        self.name_pattern = re.compile(r"<Name>(.*?)</Name>")
        self.description_pattern = re.compile(r"<Description>(.*?)</Description>")

        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[tuple[str, str, bool]]:
        try:
            output = output.replace("\n", " ")
            settlements = self.settlement_pattern.findall(output)
            areas = self.area_pattern.findall(output)
        except Exception as e:
            logger.error(f"ProvinceDecomposer. Failed to parse output: {output}")
            raise e

        parsed_locations = []

        for settlement in settlements:
            try:
                name = self.name_pattern.search(settlement).group(1)
                description = self.description_pattern.search(settlement).group(1)
                parsed_locations.append((name, description, True))
            except Exception:
                logger.error(f"ProvinceDecomposer. Can't process settlement {settlement}")
                continue

        for area in areas:
            try:
                name = self.name_pattern.search(area).group(1)
                description = self.description_pattern.search(area).group(1)
                parsed_locations.append((name, description, False))
            except Exception:
                logger.error(f"ProvinceDecomposer. Can't process area {area}")
                continue

        return parsed_locations

    def generate(self, parent_location: Province, location_tree_path: list[Region|Province]) -> list[tuple[str, str, bool]]:
        region_description = location_tree_path[0].get_description()
        province_description = parent_location.get_description()

        parsed_locations = self.chain.invoke({
            "region_description": region_description,
            "province_description": province_description
        })
        return parsed_locations
