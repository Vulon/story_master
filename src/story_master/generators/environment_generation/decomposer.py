import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel

from story_master.log import logger
from story_master.entities.location import DEFAULT_WORLD_WIDTH, DEFAULT_WORLD_HEIGHT


class BaseLocationInformation(BaseModel):
    name: str
    description: str
    x: int
    y: int


class MapDecomposer:
    PROMPT = """
    You are a map generation agent for a simulation game.
    
    -Goal-
    Create regions, that the game world is divided into.
    
    -Steps-
    1. Divide the world into several regions.
        Every region should have a separate biome.
        The map you are generating shouldn't be populated with settlements.
        Imagine, that the map doesn't have any civilization yet.
    2. Write a short description for every region, describing, what features it has.
        The description should be 1 paragraph long.
    3. Place a region on a grid cell.
        The map is a matrix of cells with the size of {world_height}x{world_width}.
        Every region should occupy a separate cell. 
        You don't need to fill every cell.
    3. Output the regions in XML format.
        For every region output the name and description.
        Format: 
        <Region>
            <Name>Region name</Name>
            <Description>Region description</Description>
            <X>Region x coordinate</X> - the int row number
            <Y>Region y coordinate</Y> - the int column number
        </Region>
        
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.name_pattern = re.compile(r"<Name>(.*?)</Name>")
        self.description_pattern = re.compile(r"<Description>(.*?)</Description>")
        self.x_pattern = re.compile(r"<X>(.*?)</X>")
        self.y_pattern = re.compile(r"<Y>(.*?)</Y>")
        self.region_pattern = re.compile(r"<Region>(.*?)</Region>")

        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[BaseLocationInformation]:
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
                x = int(self.x_pattern.search(region).group(1))
                y = int(self.y_pattern.search(region).group(1))
                parsed_regions.append(
                    BaseLocationInformation(
                        name=name, description=description, x=x, y=y
                    )
                )
            except Exception:
                logger.error(f"RootDecomposer. Can't process region {region}")
                continue
        return parsed_regions

    def generate(self) -> list[BaseLocationInformation]:
        parsed_regions = self.chain.invoke(
            {"world_height": DEFAULT_WORLD_HEIGHT, "world_width": DEFAULT_WORLD_WIDTH}
        )
        return parsed_regions
