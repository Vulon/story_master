import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.log import logger
from story_master.entities.location import Region, Object, Position

DEFAULT_GENERATION_RADIUS = 5


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
        self.object_pattern = re.compile(r"<\s*Object\s*>(.*?)</\s*Object\s*>")

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

        object_names = self.chain.invoke(
            {"region": region_description, "objects": objects_description}
        )

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
        For every object, you should generate a name, description, and size (on 2D grid).
        One cell on a grid is around 1 by 1 meter.
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

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.object_pattern = re.compile(r"<\s*Object\s*>(.*?)</\s*Object\s*>")

        self.name_pattern = re.compile(r"<\s*Name\s*>(.*?)</\s*Name\s*>")
        self.description_pattern = re.compile(
            r"<\s*Description\s*>(.*?)</\s*Description\s*>"
        )
        self.hidden_description_pattern = re.compile(
            r"<\s*HiddenDescription\s*>(.*?)</\s*HiddenDescription\s*>"
        )
        self.width_pattern = re.compile(r"<\s*Width\s*>(.*?)</\s*Width\s*>")
        self.height_pattern = re.compile(r"<\s*Height\s*>(.*?)</\s*Height\s*>")

        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[Object]:
        try:
            output = output.replace("\n", " ")
            objects = self.object_pattern.findall(output)
        except Exception as e:
            logger.error(f"ObjectGenerator: Error parsing output: {output}")
            raise e

        parsed_objects = []
        for obj in objects:
            try:
                name = self.name_pattern.search(obj).group(1)
                description = self.description_pattern.search(obj).group(1)
                hidden_description = self.hidden_description_pattern.search(obj)
                hidden_description = (
                    hidden_description.group(1) if hidden_description else None
                )
                width = int(self.width_pattern.search(obj).group(1))
                height = int(self.height_pattern.search(obj).group(1))

                parsed_objects.append(
                    Object(
                        id=0,
                        name=name,
                        description=description,
                        hidden_description=hidden_description,
                        position=Position(x=0, y=0, location_id=None),
                        width=width,
                        height=height,
                    )
                )
            except Exception:
                logger.error(f"ObjectGenerator: Can't process object {obj}")
                continue
        return parsed_objects

    def generate(self, region: Region, objects: list[str]) -> list[Object]:
        logger.info(f"Generating objects for region {region.name}")
        region_description = region.get_description()
        object_strings = "\n".join([f"<Object>{obj}</Object>" for obj in objects])
        objects_description = " ".join(object_strings)

        generated_objects = self.chain.invoke(
            {"region": region_description, "objects": objects_description}
        )

        return generated_objects


class ObjectPlacer:
    PROMPT = """
    You are a map generation agent for a simulation game.
    
    -Goal-
    Place objects on the map.
    
    -Steps-
    1. Analyze existing objects on the map.
        In rare cases, there might be no objects on the map yet.
    2. Analyze the list of objects that can be placed on the map.
    3. Place objects on the map.
        The game map is divided into regions. 
        Every region has a 2D grid with cells.
        You can only see a small part of the map at a time.
        You can place objects in a radius of {radius} cells around the grid center. 
        The positions of objects you see will be relative to the grid center.
        Every cell has a size of around 1 by 1 meter.
        You can place the same object from the provided list several times. 
        Or you can ignore some objects.
    4. Output the objects in XML format.
        For every object that you want to place, you need to output the object id, x, and y coordinates.
    
    -Existing objects-
    {existing_objects}
    
    -Placeable objects-
    {placeable_objects}
    
    -Output format-
    <Object>
        <Id>Object id</Id>
        <X>X coordinate</X>
        <Y>Y coordinate</Y>
    </Object>
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        self.object_pattern = re.compile(r"<\s*Object\s*>(.*?)</\s*Object\s*>")

        self.id_pattern = re.compile(r"<Id>(.*?)</Id>")
        self.x_pattern = re.compile(r"<X>(.*?)</X>")
        self.y_pattern = re.compile(r"<Y>(.*?)</Y>")

        prompt = PromptTemplate.from_template(self.PROMPT)
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[tuple[int, int, int]]:
        try:
            output = output.replace("\n", " ")
            objects = self.object_pattern.findall(output)
        except Exception as e:
            logger.error(f"ObjectPlacer: Error parsing output: {output}")
            raise e

        parsed_objects = []
        for obj in objects:
            try:
                id = int(self.id_pattern.search(obj).group(1))
                x = int(self.x_pattern.search(obj).group(1))
                y = int(self.y_pattern.search(obj).group(1))

                parsed_objects.append((id, x, y))
            except Exception:
                logger.error(f"ObjectPlacer: Can't process object {obj}")
                continue
        return parsed_objects

    def generate(
        self,
        region: Region,
        existing_objects: list[Object],
        placeable_objects: list[Object],
    ) -> list[Object]:
        # Don't forget to set Object ids
        # Shift the positions to the region center before placing
        # Restore the original positions after placing
        logger.info("Placing objects on the map")
        existing_object_strings = [
            f"({obj.name}: {obj.description}. Position: {obj.position.x}, {obj.position.y})"
            for obj in existing_objects
        ]
        existing_objects_description = "\n".join(existing_object_strings)
        placeable_object_strings = [obj.get_description() for obj in placeable_objects]
        placeable_objects_description = "\n".join(placeable_object_strings)

        placed_objects = self.chain.invoke(
            {
                "existing_objects": existing_objects_description,
                "placeable_objects": placeable_objects_description,
                "radius": DEFAULT_GENERATION_RADIUS,
            }
        )
        objects_table = {obj.id: obj for obj in placeable_objects}
        new_placed_objects = []
        for obj_id, x, y in placed_objects:
            if obj_id in objects_table:
                obj = objects_table[obj_id].model_copy(deep=True)
                obj.position = Position(x=x, y=y, location_id=region.id)
                new_placed_objects.append(obj)
            else:
                logger.error(
                    f"ObjectPlacer: Object with id {obj_id} is not in the placeable objects list"
                )
        return new_placed_objects
