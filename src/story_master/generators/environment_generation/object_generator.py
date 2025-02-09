import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel

from story_master.log import logger
from story_master.entities.location import BaseLocation, DEFAULT_WORLD_WIDTH, DEFAULT_WORLD_HEIGHT, Region, Object, Position


class ObjectNameGenerator:
    PROMPT = """
    You are a map generation agent for a simulation game.
    
    -Goal-
    Create objects that can be placed on the map.
    
    -Steps-
    1. Analyze the region on the map. 
    2. Analyze the list of objects already present nearby. 
        There might be a case, when there are no objects in this location yet.
    3. Generate a list of objects that can be placed in this location.
        You are generating a fresh map, that doesn't have any settlements or buildings yet. 
        Output only object, that can be found in the nature.
        For example, trees, rocks, ponds, plants, etc.
        Also don't forget to add objects, that can be harvested for resources.
        All object names should be unique.
    4. Output the objects in XML format.
    
    -Region-
    {region}
    
    -Objects-
    {objects}
    
    -Output format-
    <Object>Object name</Object>
    <Object>Second object name</Object> 
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.object_pattern = re.compile(r"<Object>(.*?)</Object>")

        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[str]:
        try:
            output = output.replace("\n", " ")
            objects = self.object_pattern.findall(output)
            return objects
        except Exception as e:
            logger.error(f"ObjectNameGenerator: Error parsing output: {output}")
            raise e

    def generate(self, region: Region, objects: list[Object]) -> list[str]:
        logger.info(f"Generating objects for region {region.name}")
        region_description = region.get_description()
        object_strings = [obj.get_description(add_description=False) for obj in objects]
        objects_description = " ".join(object_strings)

        object_names = self.chain.invoke({
            "region": region_description,
            "objects": objects_description
        })

        return object_names

class ObjectGenerator:
    PROMPT = """
    You are a map generation agent for a simulation game.
    
    -Goal-
    Create objects that can be placed on the map.
    
    -Steps-
    1. Analyze the region on the map.
    2. Analyze the list of objects already present nearby.
        There might be a case, when there are no objects in this location yet.
    3. Analyze the list of objects that can be placed in this location.
        You will have a list of object names that can be placed in this location.
    4. Generate objects with names from the list.
        For every object, you should generate a name, description, and size.
        If an object has some hidden properties, that are not visible at first sight, you should generate a hidden description.
        For example, a simple rock can be an ore deposit.
        You don't need to generate objects that are already present in the location.
    5. Output the objects in XML format.
    
    -Region-
    {region}
    
    -Objects-
    {objects}
    
    -Output format-
    <Object>
        <Name>Object name</Name>
        <Description>Object description</Description>
        <HiddenDescription>Hidden object description</HiddenDescription> - Optional
        <Width>Object width</Width>
        <Height>Object height</Height>
    </Object>
    
    Output:
    """